import os
import sys
import io
from pathlib import Path
import zipfile
import requests
from typing import List, Tuple, Dict
import tempfile
from tqdm import tqdm
from django.db import transaction
CURRENT_DIR = Path(__file__).parent

sys.path.append(str(CURRENT_DIR.parent))
sys.path.append(str(CURRENT_DIR.parent.parent))
sys.path.append(str(CURRENT_DIR.parent.parent))


import utils
from CornerStoneParser import fetch_parse_corner_stones,  update_corner_stone_status, CORNER_STONE_ID_FILENAME
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException, PARSED_TRACKS_FOLDER_NAME, PARSED_GROUPS_FOLDER_NAME

LOGGED_NOT_PARSED = 'bad.txt'
LOGGED_PARSED = 'good.txt'

utils.setup_django_pycharm()
from rest_api.models import Course, Track, CourseGroup


PARSE_RESULT_FOLDER = CURRENT_DIR

COURSE_DUMP_FILENAME = 'parsed_courses.json'
COURSE_DUMP_FILE_PATH = PARSE_RESULT_FOLDER / COURSE_DUMP_FILENAME
TRACK_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_TRACKS_FOLDER_NAME
GROUP_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_GROUPS_FOLDER_NAME


def parse_track_folder(html_folder: str, data_year: int, dump: bool = False) -> \
        Tuple[List[Dict],
              List[List[Dict]],
              List[List[int]]]:
    """
    Parses a folder of html files for tracks, returning parsed tracks, groups and course ids
    :param html_folder: folder with huji track files named `<track_id>.json`
    :param data_year: year to which the data is relevant
    :param dump: whether to dump results
    """
    # print(f'x = parsed with tracks\t (x) = parsed without track')
    all_tracks: List[Dict] = []
    all_groups: List[List[Dict]] = []
    all_course_ids: List[List[int]] = []

    for file_name in tqdm(os.listdir(html_folder)):
        track_id = int(file_name.split('.')[0])

        with open(f'{html_folder}/{file_name}', encoding='utf8') as f:
            body = f.read()

            if len(body) == 6160:  # empty file
                continue

            try:
                track, groups, courses = parse_moon(body, track_id, data_year, dump)
                all_tracks.append(track)
                all_groups.append(groups)
                all_course_ids.append(courses)

            except NoTrackParsedException:
                pass

            except ValueError as e:
                if str(e) != 'No tables found':
                    raise e

    return all_tracks, all_groups, all_course_ids


def _parse_course_details_html(file_path: str) -> Dict:
    result = None
    with open(file_path, 'rt', encoding='utf8') as open_file:
        try:
            read = open_file.read()
            result = parse_course_detail_page(read, 2021)

        except NothingToParseException:
            pass

        except Exception as e:
            print(file_path + ' ERROR ' + str(e))
            raise e

    return result


def parse_course_details_folder(dump: bool) -> List[Dict]:
    """
    Parses a folder of html files for courses, returning the course details as dictionary
    :param write_log_files: log (append) parsing staus to LOGGED_PARSED,LOGGED_NOT_PARSED
    :param dump: should dump into COURSE_DUMP_FILE, for faster (no need to parse) loading later
    :return: list of dictionaries representing courses
    """
    print('parsing course detail folder')
    results = []

    all_file_paths = [os.path.join('course_details_html', f)
                      for f in os.listdir('course_details_html')]

    nonempty_paths = [p for p in all_file_paths if os.stat(p).st_size != 29_589]

    for file_path in tqdm(nonempty_paths, desc="Parsing "):
        results.append(_parse_course_details_html(file_path))

    if dump:
        utils.dump_json(results, str(COURSE_DUMP_FILE_PATH))

    return results


def load_parsed_track_folder(folder: str = str(TRACK_DUMP_FOLDER_PATH)) -> None:

    track_file_paths = Path(folder).glob("*.json")
    track_dicts = [utils.load_json(str(path)) for path in track_file_paths]

    existing_track_numbers = [t["track_number"] for t in track_dicts]
    _, delete_dict = Track.objects.filter(track_number__in=existing_track_numbers).delete()
    print(f"Deleted and re-created conflicting track, the resulting deletion counts: {delete_dict} ")

    tracks = [Track(**dic) for dic in track_dicts]
    Track.objects.bulk_create(tracks)


def load_parsed_group(group_values: Dict) -> None:
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


def load_parsed_groups_folder(folder: str = str(GROUP_DUMP_FOLDER_PATH)):
    for f in tqdm(os.listdir(folder), desc=f"Loading parsed groups from {folder}"):
        path = os.path.join(folder,f)
        load_parsed_group(utils.load_json(path))


def load_parsed_course(course_values: Dict) -> None:
    Course.objects.update_or_create(course_id=course_values['course_id'],
                                    defaults=course_values)


def load_dumped_courses(only_add_new: bool, courses_json_file: str = str(COURSE_DUMP_FILE_PATH)) -> None:
    print(f"loading parsed courses from {courses_json_file}")

    # noinspection PyTypeChecker
    parsed = [c for c in utils.load_json(courses_json_file)
              if c is not None]  # some are None because of parsing issues

    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    existing_course_ids = [c['course_id'] for c in parsed]
    _ , delete_dict = Course.objects.filter(course_id__in=existing_course_ids).delete()
    print(f"Deleted and re-created conflicting courses, the resulting deletion counts: {delete_dict} ")
    objects = [Course(**dic) for dic in parsed]
    Course.objects.bulk_create(objects)


def parse_dump_load_all():
    parse_course_details_folder(dump=True)
    fetch_parse_corner_stones()
    parse_track_folder('tracks_html', 2021, True)  # parses groups too
    load_all_dumped()


@transaction.atomic()
def load_all_dumped(folder: Path = CURRENT_DIR):
    load_dumped_courses(only_add_new=False, courses_json_file=str(folder / COURSE_DUMP_FILENAME))
    update_corner_stone_status(id_file=str(folder / CORNER_STONE_ID_FILENAME))
    load_parsed_track_folder(folder=str(folder / PARSED_TRACKS_FOLDER_NAME))
    load_parsed_groups_folder(folder=str(folder / PARSED_GROUPS_FOLDER_NAME))

@transaction.atomic
def load_from_internet():
    print("Downloading zipped data")
    res = requests.get("https://storage.googleapis.com/closure_kb_parsed_data/parse_data_v2.zip")
    print("Extracting zipped data")
    with (zipfile.ZipFile(io.BytesIO(res.content)) as zip,
          tempfile.TemporaryDirectory(prefix="parse_state") as temp_dir):
        temp_dir = Path(temp_dir)
        zip.extractall(path=temp_dir)
        print("Done extracting zipped data, loading data into DB")
        load_all_dumped(temp_dir)   
        


if __name__ == '__main__':
    load_all_dumped()

