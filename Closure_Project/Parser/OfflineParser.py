import os
from typing import List, Tuple, Dict

from tqdm import tqdm

import utils
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException

LOGGED_NOT_PARSED = 'bad.txt'
LOGGED_PARSED = 'good.txt'

utils.setup_django_pycharm()
from rest_api.models import Course

COURSE_DUMP = 'course_dump.json'
TRACK_DUMP = 'track_dump.json'


def _parse_track_folder(html_folder: str, data_year: int, dump: bool = False) -> \
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


def _parse_course_details_html(file_name: str, write_log_files: bool) -> Dict:
    file_id = file_name[:file_name.find('.')]
    result = None
    with open(os.path.join('course_details_html', file_name), 'rt', encoding='utf8') as \
            open_file:
        try:
            read = open_file.read()
            result = parse_course_detail_page(read, 2021)

            if write_log_files:
                with open(LOGGED_PARSED, 'at') as log:
                    log.write(file_id + '\n')
            # print(f'+{file_id}')

        except NothingToParseException:
            if write_log_files:
                with open(LOGGED_NOT_PARSED, 'at') as log:
                    log.write(file_id + '\n')
            # print(f'-{file_id}')

        except Exception as e:
            print(file_name + ' ERROR ' + str(e))
            raise e

    return result


def parse_course_details_folder(read_log_files: bool,
                                write_log_files: bool,
                                dump: bool) -> List[Dict]:
    """
    Parses a folder of html files for courses, returning the course details as dictionary
    :param write_log_files: log (append) parsing staus to LOGGED_PARSED,LOGGED_NOT_PARSED
    :param read_log_files: only parse files mentioned in the LOGGED_PARSED file: parse faster!
    :param dump: should dump into COURSE_DUMP, for faster (no need to parse) loading later
    :return: list of dictionaries representing courses
    """
    print('parsing course detail folder')
    files = set(os.listdir('course_details_html'))

    if read_log_files:
        if os.path.exists(LOGGED_PARSED):
            with open(LOGGED_PARSED, 'rt') as f:
                parsable_courses = set(x.rstrip('\n') for x in f.readlines())

            print('filtering for courses from LOGGED_PARSED', end=', ')
            files = {f for f in files if f[:f.find('.')] in parsable_courses}
        else:
            print(f'either LOGGED_PARSED does not exist, parsing all instead')

    print(f'parsing {len(files)} files')
    results = []
    for file in tqdm(files):
        results.append(_parse_course_details_html(file_name=file,
                                                  write_log_files=write_log_files))

    if dump:
        utils.dump(results, COURSE_DUMP)

    return results


def insert_parsed_courses_to_db(parsed_courses: dict) -> None:
    print('inserting parsed courses to db')
    for course in tqdm(parsed_courses):
        Course.objects.update_or_create(**course)


def insert_dumped_courses_to_db(only_add_new: bool) -> None:
    # noinspection PyTypeChecker
    parsed = utils.load(COURSE_DUMP)
    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    insert_parsed_courses_to_db(parsed)


def parse_all():
    # parse_course_details_folder(read_log_files=True, write_log_files=True, dump=True)
    # insert_dumped_courses_to_db(True)
    # fetch_insert_corner_stones_to_db()
    _parse_track_folder('tracks_html', 2021, True)


if __name__ == '__main__':
    parse_all()
