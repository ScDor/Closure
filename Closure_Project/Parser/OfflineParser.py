from functools import partial
from pathlib import Path
from typing import List, Tuple, Dict
from tqdm import tqdm

from utils import dump_json
from CornerStoneParser import fetch_parse_corner_stones
from MoonParser import parse_course_detail_page, NothingToParseException, parse_moon, \
    NoTrackParsedException, PARSED_TRACKS_FOLDER_NAME, PARSED_GROUPS_FOLDER_NAME

from tqdm.contrib.concurrent import process_map

CURRENT_DIR = Path(__file__).parent
PARSE_RESULT_FOLDER = CURRENT_DIR

COURSE_DUMP_FILENAME = 'parsed_courses.json'
COURSE_DUMP_FILE_PATH = PARSE_RESULT_FOLDER / COURSE_DUMP_FILENAME
TRACK_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_TRACKS_FOLDER_NAME
GROUP_DUMP_FOLDER_PATH = PARSE_RESULT_FOLDER / PARSED_GROUPS_FOLDER_NAME

PARSED_DATA_ZIP_PATH = CURRENT_DIR / "parse_data.zip"
PARSED_DATA_ZIP_URL = "https://storage.googleapis.com/closure_kb_parsed_data/parse_data.zip"


def parse_track_folder(data_year: int, dump: bool = False) -> \
        Tuple[List[Dict],
              List[List[Dict]],
              List[List[int]]]:
    """
    Parses a folder of html files for tracks, returning parsed tracks, groups and course ids
    :param data_year: year to which the data is relevant
    :param dump: whether to dump results
    """
    # print(f'x = parsed with tracks\t (x) = parsed without track')
    all_tracks: List[Dict] = []
    all_groups: List[List[Dict]] = []
    all_course_ids: List[List[int]] = []

    html_folder = Path(f"{data_year}_tracks")

    for file in tqdm(list(html_folder.glob("*.html")), desc=f"Parsing {data_year} tracks"):
        track_id = int(file.stem)

        with open(file, encoding='utf8') as f:
            body = f.read()

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


def _parse_course_details_html(file_path: str, data_year: int) -> Dict:
    result = None
    with open(file_path, 'rt', encoding='utf8') as open_file:
        try:
            read = open_file.read()
            result = parse_course_detail_page(read, data_year)

        except NothingToParseException:
            print(f"Nothing to parse on {file_path}")

        except Exception as e:
            print(str(file_path) + ' ERROR ' + str(e))
            raise e

    return result


def parse_course_details_folder(data_year: int, dump: bool) -> List[Dict]:
    """
    Parses a folder of html files for courses, returning the course details as dictionary
    :param data_year: data year
    :param dump: should dump into COURSE_DUMP_FILE, for faster (no need to parse) loading later
    :return: list of dictionaries representing courses
    """
    html_folder = Path(f"{data_year}_courses")

    parser = partial(_parse_course_details_html, data_year=data_year)
    results = process_map(parser,
                          list(html_folder.glob("*.html")),
                          desc=f"Parsing {data_year} courses",
                          chunksize=1)

    if dump:
        dump_json(results, str(COURSE_DUMP_FILE_PATH), extend=True)

    return results


def parse_all(data_year: int):
    parse_course_details_folder(data_year, dump=True)
    fetch_parse_corner_stones()
    parse_track_folder(data_year, dump=True)  # parses groups too
