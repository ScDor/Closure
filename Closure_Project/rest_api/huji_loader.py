import io
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Dict

import requests
from django.conf import settings
from django.db import transaction
from tqdm import tqdm

from Parser.CornerStoneParser import CORNER_STONE_ID_FILENAME, CORNER_STONE_ID_FILE_PATH
from Parser.MoonParser import PARSED_TRACKS_FOLDER_NAME, PARSED_GROUPS_FOLDER_NAME
from Parser.OfflineParser import TRACK_DUMP_FOLDER_PATH, GROUP_DUMP_FOLDER_PATH, \
    COURSE_DUMP_FILE_PATH, CURRENT_DIR, \
    COURSE_DUMP_FILENAME, PARSED_DATA_ZIP_PATH, PARSED_DATA_ZIP_URL
from rest_api.models import Track, CourseGroup, Course
from utils import load_json

MAX_BATCH_SIZE = None
if settings.DATABASES['default']['ENGINE'] == "django.db.backends.sqlite3":
    MAX_BATCH_SIZE = 250
    print("Shrinking batch size because we're using SQLite")


def import_tracks(folder: str = str(TRACK_DUMP_FOLDER_PATH)) -> None:
    track_dicts = []
    year_folders = list(Path(folder).iterdir())
    for year_folder in tqdm(year_folders, desc="Loading tracks JSONs from each year, into memory"):
        assert year_folder.is_dir(), "parsed_tracks folder should consist of a folder of each year"
        track_objects = [load_json(str(track_file)) for track_file in year_folder.iterdir()]
        track_objects = [{**obj, "data_year": year_folder.name} for obj in track_objects]
        track_dicts.extend(track_objects)

    tracks = [Track(**dic) for dic in track_dicts]
    Track.objects.bulk_create(tracks, batch_size=MAX_BATCH_SIZE)


def import_course_group(group_values: Dict) -> None:
    track_id = group_values['track_id']
    track = Track.objects.get(track_number=track_id, data_year=group_values['data_year'])
    del group_values['track_id']

    group_values['track'] = track

    course_ids = group_values['course_ids']
    del group_values['course_ids']

    group, _ = CourseGroup.objects.update_or_create(
        track=track,
        year_in_studies=group_values['year_in_studies'],
        index_in_track_year=group_values['index_in_track_year'],
        defaults=group_values)

    group.courses.set(Course.objects.filter(course_id__in=course_ids))
    group.save()


def import_course_groups(folder: str = str(GROUP_DUMP_FOLDER_PATH)):
    print(f"Loading course group JSONs")
    cg_dicts = []
    year_folders = list(Path(folder).iterdir())
    for year_folder in tqdm(year_folders, desc="Loading course group JSONs from each year, into memory"):
        assert year_folder.is_dir(), "parsed_groups folder should consist of a folder of each year"
        cg_objects = [load_json(str(cg_file)) for cg_file in year_folder.iterdir()]
        cg_objects = [{**obj, "data_year": year_folder.name} for obj in cg_objects]
        cg_dicts.extend(cg_objects)

    print(f"Loaded {len(cg_dicts)} jsons")

    with transaction.atomic():
        for cg_dict in tqdm(cg_dicts, desc="importing coursegroups to SQL"):
            import_course_group(cg_dict)


def import_courses(only_add_new: bool,
                   courses_json_file: str = str(COURSE_DUMP_FILE_PATH)) -> None:
    print(f"loading parsed courses from {courses_json_file}")

    # noinspection PyTypeChecker
    parsed = [c for c in load_json(courses_json_file)
              if c is not None]  # some are None because of parsing issues

    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    objects = [Course(**dic) for dic in parsed]
    Course.objects.bulk_create(objects, batch_size=MAX_BATCH_SIZE)


def update_corner_stone_status(
        corner_stone_id_file: str = str(CORNER_STONE_ID_FILE_PATH)) -> None:
    """
    Updates the corner stone status of pre-existing courses via a file of corner stone course IDs.
    """
    old_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)}
    print(f'before parsing, {len(Course.objects.filter(is_corner_stone=True))} '
          f'courses are marked as corner stone')

    parsed = load_json(corner_stone_id_file)

    courses = Course.objects.filter(course_id__in=parsed)
    for course in courses:
        course.is_corner_stone = True
        course.save(update_fields=['is_corner_stone'])

    new_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)
                         if c.course_id not in old_corner_stones}
    print(f'after parsing, {len(new_corner_stones)} new courses marked as corner stone: '
          f'{new_corner_stones}')


@transaction.atomic()
def load_everything(folder: Path = CURRENT_DIR):
    import_courses(only_add_new=False, courses_json_file=str(folder / COURSE_DUMP_FILENAME))
    update_corner_stone_status(corner_stone_id_file=str(folder / CORNER_STONE_ID_FILENAME))
    import_tracks(folder=str(folder / PARSED_TRACKS_FOLDER_NAME))
    import_course_groups(folder=str(folder / PARSED_GROUPS_FOLDER_NAME))


def load_from_zip(zip_file=PARSED_DATA_ZIP_PATH):
    with zipfile.ZipFile(zip_file) as zipf, \
            tempfile.TemporaryDirectory(prefix="parse_state") as temp_dir:
        temp_dir = Path(temp_dir)
        print("Extracting zipped data")
        zipf.extractall(path=temp_dir)
        print("Done extracting zipped data, loading data into DB")
        load_everything(temp_dir)


def load_from_internet(url: str = PARSED_DATA_ZIP_URL):
    print("Downloading zipped data")
    res = requests.get(url)
    if not res.ok:
        raise Exception(
            f"Couldn't retrieve zip_file from GCS bucket: {res.status_code} - {res.text}")
    load_from_zip(io.BytesIO(res.content))
