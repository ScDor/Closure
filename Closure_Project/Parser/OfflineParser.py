import os
from pathlib import Path
from typing import List, Tuple, Dict
from tqdm import tqdm


CURRENT_DIR = Path(__file__).parent


import utils
from CornerStoneParser import fetch_parse_corner_stones
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException, PARSED_TRACKS_FOLDER_NAME, PARSED_GROUPS_FOLDER_NAME

LOGGED_NOT_PARSED = 'bad.txt'
LOGGED_PARSED = 'good.txt'


PARSE_RESULT_FOLDER = CURRENT_DIR

COURSE_DUMP_FILENAME = 'parsed_courses.json'
COURSE_DUMP_FILE_PATH = PARSE_RESULT_FOLDER / COURSE_DUMP_FILENAME
TRACK_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_TRACKS_FOLDER_NAME
GROUP_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_GROUPS_FOLDER_NAME


PARSED_DATA_ZIP_PATH = CURRENT_DIR / "parse_data.zip"
PARSED_DATA_ZIP_URL = "https://storage.googleapis.com/closure_kb_parsed_data/parse_data.zip"

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


def parse_dump_load_all():
    parse_course_details_folder(dump=True)
    fetch_parse_corner_stones()
    parse_track_folder('tracks_html', 2021, True)  # parses groups too


if __name__ == '__main__':
    parse_dump_load_all()
