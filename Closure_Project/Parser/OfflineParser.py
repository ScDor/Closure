import os
from typing import List, Tuple, Dict

from tqdm import tqdm

import rest_api.models
import utils
from CornerStoneParser import fetch_insert_corner_stones_into_db
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException

LOGGED_NOT_PARSED = 'bad.txt'
LOGGED_PARSED = 'good.txt'

utils.setup_django_pycharm()
from rest_api.models import Course, Track, CourseGroup, PrerequisiteList

COURSE_DUMP = 'parsed_courses.json'


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
    :param dump: should dump into COURSE_DUMP, for faster (no need to parse) loading later
    :return: list of dictionaries representing courses
    """
    print('parsing course detail folder')
    results = []

    all_file_paths = [os.path.join('course_details_html', f)
                      for f in os.listdir('course_details_html')]

    nonempty_paths = [p for p in all_file_paths if os.stat(p).st_size != 29_589]

    for file_path in tqdm(nonempty_paths):
        results.append(_parse_course_details_html(file_path))

    if dump:
        utils.dump_json(results, COURSE_DUMP)

    return results


def load_parsed_track(track_values: Dict) -> None:
    # print('inserting track #' + str(track_values['track_number']))
    Track.objects.update_or_create(**track_values)


def load_parsed_track_folder(folder: str = 'parsed_tracks') -> None:
    for f in tqdm(os.listdir(folder)):
        load_parsed_track(utils.load_json(os.path.join(folder, f)))


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


def load_parsed_groups_folder(folder_path: str = 'parsed_groups'):
    for f in tqdm(os.listdir(folder_path)):
        path = os.path.join(folder_path, f)
        load_parsed_group(utils.load_json(path))


def load_parsed_course(course_values: Dict) -> None:
    if 'prerequisites' in course_values:
        del course_values['prerequisites']

    Course.objects.update_or_create(course_id=course_values['course_id'],
                                    defaults=course_values)


def _load_prerequisites_single(course_id: int, data_year: int,
                               prerequisites: List[List[dict]]):
    # prerequisite_values format example:
    # [
    #   [{"course_id": 67504, "min_grade": 0}], [{"course_id": 67577, "min_grade": 0}],
    #   [{"course_id": 80420, "min_grade": 0}, {"course_id": 80430, "min_grade": 0}]
    # ]
    prerequisites = list(filter(None, prerequisites))
    if not prerequisites:
        return

    course = Course.objects.get(course_id=course_id, data_year=data_year)
    prerequisite_group_object = PrerequisiteList.objects.create()

    for prerequisite_group in prerequisites:
        for req_course in prerequisite_group:
            prerequisite_course_id = req_course['course_id']
            try:
                course_object = Course.objects.get(course_id=prerequisite_course_id,
                                                   data_year=data_year)
                prerequisite_group_object.take_one_of.add(course_object)
            except rest_api.models.Course.DoesNotExist:
                print(f'Warning! course #{prerequisite_course_id} is a prerequisite for #'
                      f'{course_id} but does not exist in the system! Skipping prerequisite')
        prerequisite_group_object.save()
    course.save()


def load_dumped_courses(only_add_new: bool) -> None:
    print('loading parsed courses to db')
    # noinspection PyTypeChecker
    parsed = [value for value in utils.load_json(COURSE_DUMP)
              if value is not None]  # some are None because of parsing issues

    if only_add_new:
        existing_ids = {v[1] for v in Course.objects.values_list()}
        parsed = [p for p in parsed if p and p['course_id'] not in existing_ids]

    # for course_values in tqdm(parsed):
    #     load_parsed_course(course_values)

    for course_values in tqdm(parsed):
        # separate loop on purpose, as all courses must exist to create prerequisites
        _load_prerequisites_single(course_id=course_values['course_id'],
                                   data_year=course_values['data_year'],
                                   prerequisites=course_values['prerequisites'])


def parse_dump_load_all():
    parse_course_details_folder(dump=True)
    fetch_insert_corner_stones_into_db()
    parse_track_folder('tracks_html', 2021, True)  # parses groups too

    load_all_dumped()


def load_all_dumped():
    load_dumped_courses(False)
    fetch_insert_corner_stones_into_db()
    load_parsed_track_folder()
    load_parsed_groups_folder()


if __name__ == '__main__':
    load_dumped_courses(False)
