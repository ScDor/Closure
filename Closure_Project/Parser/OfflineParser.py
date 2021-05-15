import json
import os
from typing import List, Tuple

import utils

utils.setup_django_pycharm()

from rest_api.models import Course, CourseGroup, Track
from MoonParser import parse_moon, NoTrackParsedException

DUMP_FILE = 'dump.json'


def parse(json_folder: str, data_year: int, dump: bool = False) -> \
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
        utils.dump((all_courses, all_groups, all_tracks, all_track_ids), DUMP_FILE)

    return all_courses, all_groups, all_tracks, all_track_ids


def load():
    all_courses, all_groups, all_tracks, ids = utils.load(DUMP_FILE)
    CourseGroup.objects.update_or_create()

if __name__ == '__main__':
    parse('tracks', 2021, True)
