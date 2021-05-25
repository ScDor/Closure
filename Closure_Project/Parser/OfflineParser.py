import json
import os
from typing import List, Tuple, Dict

from tqdm import tqdm

import utils
from CornerStoneParser import fetch_insert_corner_stones_to_db
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException

utils.setup_django_pycharm()
from rest_api.models import Course, CourseGroup, Track

COURSE_DUMP = 'course_dump.json'
TRACK_DUMP = 'track_dump.json'


def _parse_tracks(html_folder: str, data_year: int, dump: bool = False) -> \
        Tuple[List[List[Course]], List[List[CourseGroup]], List[Track], List[str]]:
    """
    Parses and inserts parsed into the database
    :param html_folder: folder with huji track files named `<track_id>.json`
    :param data_year: year to which the data is relevant
    :param dump: whether to dump results to a jsonpickle file (for faster later processing)
    """
    # print(f'x = parsed with tracks\t (x) = parsed without track')
    all_tracks: List[Track] = []
    all_courses: List[List[Course]] = []
    all_groups: List[List[CourseGroup]] = []
    all_track_ids: List[str] = []

    for file_name in tqdm(os.listdir(html_folder)):
        with open(rf'{html_folder}/{file_name}', 'r', encoding='utf8') as openf:
            track_id = int(file_name.split('.')[0])
            body = openf.read()

            if len(body) == 6160:  # empty file
                continue

            parsed_track = False

            try:
                track, courses, groups = parse_moon(body, track_id, data_year)
                all_tracks.append(track)
                all_courses.append(courses)
                all_groups.append(groups)
                parsed_track = True

            except NoTrackParsedException as e:
                pass

            except ValueError as e:
                if str(e) != 'No tables found':
                    raise e

            file_name = file_name.split('.')[0]
            formatted_track_id = file_name if parsed_track else f'({file_name})'
            all_track_ids.append(formatted_track_id)
            # print(formatted_track_id, end=', ')

    if dump:
        utils.dump((all_courses, all_groups, all_tracks, all_track_ids), TRACK_DUMP)

    return all_courses, all_groups, all_tracks, all_track_ids


def _parse_course_details_html(file_name: str, write_status_to_file: bool = False) -> Dict:
    # print(file_name)
    file_id = file_name[:file_name.find('.')]
    result = None
    with open(os.path.join('course_details', file_name), 'rt', encoding='utf8') as open_file:
        try:
            read = open_file.read()
            result = parse_course_detail_page(read, 2021)

            if write_status_to_file:
                with open('good.txt', 'at') as log:
                    log.write(file_id + '\n')
            # print(f'+{file_id}')

        except NothingToParseException:
            if write_status_to_file:
                with open('bad.txt', 'at') as log:
                    log.write(file_id + '\n')
            # print(f'-{file_id}')

        except Exception as e:
            print(file_name + ' ERROR ' + str(e))
            raise e

    return result


def load_tracks():
    all_courses, all_groups, all_tracks, ids = utils.load(TRACK_DUMP)


def parse_course_details_folder(read_log_files: bool, dump: bool) \
        -> List[Dict]:
    print('parsing course detail folder')
    files = set(os.listdir('course_details'))

    if read_log_files:
        if os.path.exists('good.txt') and os.path.exists('bad.txt'):
            with open('good.txt', 'rt') as f:
                good = set(x.rstrip('\n') for x in f.readlines())

            with open('bad.txt', 'rt') as f:
                bad = set(x.rstrip('\n') for x in f.readlines())

            print('filtering for files only in good.txt', end=', ')
            files = {f for f in files if f[:f.find('.')] in good}
        else:
            print(f'either good.txt or bad.txt do not exist, ignoring read_log_files')

    print(f'parsing {len(files)} files')
    results = []
    for file in tqdm(files):
        results.append(_parse_course_details_html(file))

    if dump:
        with open(COURSE_DUMP, 'w', encoding='utf8') as f:
            json.dump(results, f)

    return results


def insert_parsed_courses_to_db(parsed_wfr: dict) -> None:
    print('inserting parsed courses to db')
    for course in tqdm(parsed_wfr):
        Course.objects.update_or_create(**course)


def insert_dumped_courses_to_db(only_add_new: bool) -> None:
    with open(COURSE_DUMP, 'r', encoding='utf8') as f:
        parsed = json.load(f)

    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    insert_parsed_courses_to_db(parsed)


def parse_all():
    parse_course_details_folder(True,True)
    insert_dumped_courses_to_db(True)
    fetch_insert_corner_stones_to_db()
    _parse_tracks('tracks', 2021)


if __name__ == '__main__':
    parse_all()
