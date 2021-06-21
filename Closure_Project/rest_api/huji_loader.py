import io
import os
import zipfile
from pathlib import Path
from typing import Dict, Union, IO
from tqdm import tqdm
import tempfile
import json

import requests
from django.db import transaction

from Parser.CornerStoneParser import CORNER_STONE_ID_FILENAME, CORNER_STONE_ID_FILE_PATH
from Parser.MoonParser import PARSED_TRACKS_FOLDER_NAME, PARSED_GROUPS_FOLDER_NAME
from Parser.OfflineParser import TRACK_DUMP_FOLDER_PATH, GROUP_DUMP_FOLDER_PATH, COURSE_DUMP_FILE_PATH, CURRENT_DIR, \
    COURSE_DUMP_FILENAME, PARSED_DATA_ZIP_PATH, PARSED_DATA_ZIP_URL
from rest_api.models import Track, CourseGroup, Course


def import_tracks(folder: str = str(TRACK_DUMP_FOLDER_PATH)) -> None:

    track_file_paths = Path(folder).glob("*.json")
    track_dicts = [load_json(str(path)) for path in track_file_paths]

    existing_track_numbers = [t["track_number"] for t in track_dicts]
    _, delete_dict = Track.objects.filter(track_number__in=existing_track_numbers).delete()
    print(f"Deleted and re-created conflicting tracks, the resulting deletion counts: {delete_dict} ")

    tracks = [Track(**dic) for dic in track_dicts]
    Track.objects.bulk_create(tracks)


def import_course_group(group_values: Dict) -> None:
    track_id = group_values['track_id']
    track = Track.objects.get(track_number=track_id)
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
    for f in tqdm(os.listdir(folder), desc=f"Loading parsed groups from {folder}"):
        path = os.path.join(folder,f)
        import_course_group(load_json(path))


def import_courses(only_add_new: bool, courses_json_file: str = str(COURSE_DUMP_FILE_PATH)) -> None:
    print(f"loading parsed courses from {courses_json_file}")

    # noinspection PyTypeChecker
    parsed = [c for c in load_json(courses_json_file)
              if c is not None]  # some are None because of parsing issues

    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    existing_course_ids = [c['course_id'] for c in parsed]
    _ , delete_dict = Course.objects.filter(course_id__in=existing_course_ids).delete()
    print(f"Deleted and re-created conflicting courses, the resulting deletion counts: {delete_dict} ")
    objects = [Course(**dic) for dic in parsed]
    Course.objects.bulk_create(objects)


def update_corner_stone_status(id_file: str = str(CORNER_STONE_ID_FILE_PATH)) -> None:
    """
    Updates the corner stone status of pre-existing courses via a file of corner stone course IDs.
    """
    old_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)}
    print(f'before parsing, {len(Course.objects.filter(is_corner_stone=True))} '
          f'courses are marked as corner stone')

    parsed = load_json(id_file)

    for course_id in parsed:
        course = Course.objects.get(course_id=course_id)
        course.is_corner_stone = True
        course.save(update_fields=['is_corner_stone'])

    new_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)
                         if c.course_id not in old_corner_stones}
    print(f'after parsing, {len(new_corner_stones)} new courses marked as corner stone: '
          f'{new_corner_stones}')


@transaction.atomic()
def load_everything(folder: Path = CURRENT_DIR):
    import_courses(only_add_new=False, courses_json_file=str(folder / COURSE_DUMP_FILENAME))
    update_corner_stone_status(id_file=str(folder / CORNER_STONE_ID_FILENAME))
    import_tracks(folder=str(folder / PARSED_TRACKS_FOLDER_NAME))
    import_course_groups(folder=str(folder / PARSED_GROUPS_FOLDER_NAME))


def load_from_zip(zip_file: Union[IO[bytes], os.PathLike[str]] = PARSED_DATA_ZIP_PATH):
    with zipfile.ZipFile(zip_file) as zipf,\
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
        raise Exception(f"Couldn't retrieve zip_file from GCS bucket: {res.status_code} - {res.text}")
    load_from_zip(io.BytesIO(res.content))


def setup_django_pycharm():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
    import django
    django.setup()


def load_json(filename: str):
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


if __name__ == "__main__":
    setup_django_pycharm()
    load_from_zip()

