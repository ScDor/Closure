import logging
import re
from typing import List

import pandas as pd
import requests

from Parser.Types import Year, Semester, CourseType, Course

# hebrew titles as they appear on http://bit.ly/course_details_3010
COURSE_ID_HEB = 'מספר הקורס'
COURSE_NAME_HEB = 'שם הקורס'
POINTS_HEB = 'נקודות זכות'
SEMESTER_HEB = 'סמסטר'
MAX_YEAR_HEB = 'עד שנה'  # does not always appear
IS_ELEMENTARY_HEB = 'קורס יסוד'  # does not always appear
HUG_ID_HEB = 'שיוך לחוג'

# english versions of the titles, to be used project-wide
COURSE_ID = 'course_id'
COURSE_NAME = 'course_name'
POINTS = 'points'
SEMESTER = 'semester'
MAX_YEAR = 'until_year'  # does not always appear
IS_ELEMENTARY = 'is_elementary'  # does not always appear
HUG_ID = 'belongs_to_hug'
YEAR = 'year'
TYPE = 'course_type'

HEB_ENG_TITLES = {
    COURSE_ID_HEB: COURSE_ID,
    COURSE_NAME_HEB: COURSE_NAME,
    POINTS_HEB: POINTS,
    SEMESTER_HEB: SEMESTER,
    MAX_YEAR_HEB: MAX_YEAR,
    IS_ELEMENTARY_HEB: IS_ELEMENTARY,
    HUG_ID_HEB: HUG_ID
}

YEAR_STRINGS = {
    'שנה א\'': Year.A,
    'שנה ב\'': Year.B,
    'שנה ג\'': Year.C,
    'שנה ד\'': Year.D,
    'שנה ה\'': Year.E,
    'שנה ו\'': Year.F,
    'שנה ז\'': Year.G
}

SEMESTER_STRINGS = {
    'א\'': Semester.A,
    'ב\'': Semester.B,
    'א\' או ב\'': Semester.EITHER,
    'קורס שנתי': Semester.ANNUAL,
    'קיץ': Semester.SUMMER
}

COURSE_TYPE_STRINGS = {
    'לימודי חובה': CourseType.MUST,
    'לימודי חובת בחירה': CourseType.FROM_LIST,
    'קורסי בחירה': CourseType.CHOICE
}

IGNORABLE_TITLES = {'סה\"כ נקודות חובה', 'תוכנית הלימודים'} | {y[:-1] for y in YEAR_STRINGS}

# column names on tables representing course details
COURSE_DETAILS_TITLES = {COURSE_NAME_HEB, COURSE_ID_HEB, POINTS_HEB, SEMESTER_HEB}


def parse_year(string: str) -> Year:
    """
    :param string: represents a year
    :return: Year object
    """
    try:
        return YEAR_STRINGS[string.strip()]
    except KeyError:
        raise NotImplementedError(f"can not parse year from {string}")


def parse_semester(string: str) -> Semester:
    """
    :param string: semester description
    :return: a Semester object
    """
    try:
        return SEMESTER_STRINGS[string.strip()]
    except KeyError:
        raise NotImplementedError(f"can not parse semester from {string}")


def parse_course_type(string: str) -> CourseType:
    """
    :param string: course course_type description
    :return: a CourseType object
    """
    try:
        return COURSE_TYPE_STRINGS[string.strip()]
    except KeyError:
        raise NotImplementedError(f"can not parse course course_type from {string}")


def parse_min_points(string: str) -> int:
    """
    :param string: of format "must take at least x points" (see regex)
    :return: number of points parsed, else ValueError
    """
    match = re.match(r'יש לבחור לפחות (\d+) נ\"?(?:ז|נקודות)', string)
    if match:
        min_points = int(match.group(1))
        logging.info(f'parsed min_points={min_points}')
        return min_points
    raise ValueError(f"string does not match minimum point regex: {string}")


def parse_min_courses(string: str) -> int:
    """
    :param string: of format "must take at least x courses" (see regex)
    :return: number of courses parsed, else ValueError
    """
    min_courses = None

    if "לפחות קורס 1" in string:
        min_courses = 1

    else:
        match = re.match(r'יש לבחור לפחות (\d+) קורסים.*', string)
        if match:
            logging.info(f'parsed min_courses=1')
            min_courses = match.group(1)

    if min_courses:
        return min_courses
    raise ValueError(f"string does not match minimum course regex: {string}")


def _compose_moon_url(track_id: int,
                      year: int = 2021,
                      faculty: int = 2,
                      entity_id: int = 521,
                      chug_id: int = 521,
                      degree_code: int = 71
                      ):
    """

    :param faculty: Faculty code #todo list known codes
    :param entity_id: seems to be tied with chug_id
    :param track_id: the important part, seemingly the only one that matters.
     for extended CS major use 23010
    :param year: Shnaton year to fetch
    :param chug_id: Seems to have little/no effect on parsed data
    :param degree_code: Seems to have little/no effect on parsed data
    :return:
    """
    # noinspection HttpUrlsUsage
    # NOTE: moon only works over HTTP
    return f'http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx?' \
           f'year={year}' \
           f'&faculty={faculty}' \
           f'&entityId={entity_id}' \
           f'&chugId={chug_id}' \
           f'&degreeCode={degree_code}' \
           f'&maslulId={track_id}'


def parse_course_details(df: pd.DataFrame, year: Year, course_type: CourseType) -> \
        List[Course]:
    """
    parses a table of course details, given previously-parsed Year and CourseType
    :param df: dataframe of course details
    :param year: year in studies, parsed from a previous table
    :param course_type: CourseType, parsed from a previous table
    :return: dataframe of courses
    """
    df.columns = [HEB_ENG_TITLES[title] for title in df.loc[0]]
    df = df.drop(0)
    parsed_courses = []

    df[SEMESTER] = df[SEMESTER].apply(parse_semester)
    df[COURSE_ID] = df[COURSE_ID].astype(int)
    df[HUG_ID] = df[HUG_ID].astype(int)
    df[POINTS] = df[POINTS].astype(float)
    if MAX_YEAR in df:
        df[MAX_YEAR] = df[MAX_YEAR].astype(int)
    if IS_ELEMENTARY in df:
        df[IS_ELEMENTARY] = df[IS_ELEMENTARY].apply(lambda x: None if pd.isna(x) else x)

    to_dict = df.T.to_dict().values()

    for row in to_dict:
        parsed_courses.append(
            Course(course_id=row[COURSE_ID],
                   course_type=course_type,
                   name=row[COURSE_NAME],
                   hug_id=row[HUG_ID],
                   points=row[POINTS],
                   semester=row[SEMESTER],
                   year=year,
                   max_year=row[MAX_YEAR] if MAX_YEAR in df else None,
                   is_elementary=row[IS_ELEMENTARY] if IS_ELEMENTARY in df else None))

    return parsed_courses


def parse_moon(url: str):
    """ parses a page from HUJI-MOON, see _compose_moon_url() """
    df_list = pd.read_html(requests.get(url).text)

    current_year = None
    current_type = None

    parsed_courses = []

    for i, table in enumerate(df_list):
        titles = table.loc[0]

        first_value = table.iloc[0, 0].strip()
        logging.debug(f'read a {table.shape} table, first vale={first_value}')

        if first_value in IGNORABLE_TITLES:
            logging.info(f'ignoring {first_value}')

        elif table.shape == (1, 1):  # only one cell
            if first_value in YEAR_STRINGS:
                current_year = parse_year(first_value)
                logging.debug(f'year={current_year}')

            elif first_value in COURSE_TYPE_STRINGS:
                current_type = parse_course_type(first_value)
                logging.debug(f'course_type={current_type}')

            elif 'לפחות' in first_value:
                if any(s in first_value for s in {'נ\"ז', ' נקודות '}):
                    logging.debug(f'min_points={parse_min_points(first_value)}')

                elif 'קורס' in first_value:
                    logging.debug(f'min_courses={parse_min_courses(first_value)}')

                else:
                    raise ValueError(
                        f'failed parsing min_courses or min_points from {first_value}')

        elif COURSE_DETAILS_TITLES.issubset(titles):
            if current_year is None or current_type is None:
                raise NotImplementedError("reached course details before parsing"
                                          " current year/course course_type")
            # noinspection PyTypeChecker
            newly_parsed_courses = parse_course_details(table, current_year, current_type)

            logging.debug(f'parsed {len(newly_parsed_courses)} courses')
            parsed_courses.extend(newly_parsed_courses)

        else:
            logging.info(f'Could not parse anything from table #{i} of size {table.shape}'
                         f'on {url}, starting with {table.iloc[0, 0]}.'
                         f' This is not necessarily a bad thing.')

    return parsed_courses
