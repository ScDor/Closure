import json
import os
from typing import List, Tuple

from MoonParser import parse_course_wfr_page, NothingToParseException ,parse_moon, NoTrackParsedException
import utils

utils.setup_django_pycharm()
from rest_api.models import Course, CourseGroup, Track

TRACK_DUMP = 'track_dump.json'


def parse_tracks(json_folder: str, data_year: int, dump: bool = False) -> \
        Tuple[List[List[Course]], List[List[CourseGroup]], List[Track], List[str]]:
    """
    Parses and inserts parsed into the database
    :param json_folder: folder with huji track files named `<track_id>.json`
    :param data_year: year to which the data is relevant
    :param dump: whether to dump results to a jsonpickle file (for faster later processing)
    """
    print(f'x = parsed with tracks\t (x) = parsed without track')
    all_tracks: List[Track] = []
    all_courses: List[List[Course]] = []
    all_groups: List[List[CourseGroup]] = []
    all_track_ids: List[str] = []

    for file_name in os.listdir(json_folder):
        with open(rf'{json_folder}/{file_name}', 'r') as openf:
            track_id = int(file_name.split('.')[0])
            body = json.load(openf)

            if len(body) == 6244:  # empty file
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
            print(formatted_track_id, end=', ')

    if dump:
        utils.dump((all_courses, all_groups, all_tracks, all_track_ids), TRACK_DUMP)

    return all_courses, all_groups, all_tracks, all_track_ids


def parse_corner_stones():
    pass


def parse_wfr(file_name: str, write_status_to_file: bool = False):
    print(file_name)
    file_id = file_name[:file_name.find('.')]

    with open(os.path.join('course_wfr', file_name), 'rt', encoding='utf8') as open_file:
        try:
            read = open_file.read()
            parse_course_wfr_page(read, 2021)

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


def load():
    all_courses, all_groups, all_tracks, ids = utils.load(TRACK_DUMP)


if __name__ == '__main__':
    with open('good.txt', 'rt') as f:
        good = set(x.rstrip('\n') for x in f.readlines())

    with open('bad.txt', 'rt') as f:
        bad = set(x.rstrip('\n') for x in f.readlines())

    seen = good | bad

    files = {f for f in os.listdir('course_wfr') if f[:f.find('.')] in good}
    print(f'working on {len(files)} files')

    # with Pool() as pool:
    #     pool.map(parse_wfr, files)

    for file in files:
        parse_wfr(file)
