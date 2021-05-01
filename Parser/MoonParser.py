import re
from datetime import datetime
from typing import List, Tuple

import pandas as pd

from data_structures import Year, Semester, CourseType, Course, CourseGroup, Track

# hebrew titles as they appear on http://bit.ly/course_details_3010
MIN_POINTS_PATTERN = re.compile(r'לפחות\s*(\d+)\s*נ')
MIN_COURSES_PATTERN = re.compile(r'יש ללמוד.*(\d+) מתוך רשימת קורסים')
MIN_COURSES_ONE_PATTERN = re.compile(r'לפחות קורס 1\s|את אחד')
MAX_COURSES_ONE_PATTERN = re.compile(r'אחד לכל היותר|רק קורס 1')
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
    'קורס קיץ': Semester.SUMMER
}

COURSE_TYPE_STRINGS = {
    'לימודי חובה': CourseType.MUST,
    'לימודי חובת בחירה': CourseType.FROM_LIST,
    'קורסי בחירה': CourseType.CHOICE
}

IGNORABLE_TITLES = {
    'סה\"כ נקודות חובה',
    'תוכנית הלימודים',
    'וגם',
    'או'  # todo handle alternatives
}

# column names on tables representing course details
COURSE_DETAILS_TITLES = {COURSE_NAME_HEB, COURSE_ID_HEB, POINTS_HEB, SEMESTER_HEB}

MUST = 'חובה'
MUST_IN_HUG = 'חובה בחוג'
MUST_PROGRAMMING = 'לימודי תכנות'
MUST_SAFETY_LIBRARY = 'קורס ספרייה ובטיחות'

CHOICE_FROM_LIST = 'חובת בחירה'
CHOICE_IN_HUG = 'בחירה בחוג'
CORNER_STONES = 'אבני פינה'
COMPLEMENTARY = 'לימודים משלימים'
ADDITIONAL_HUG = 'חוג נוסף'
HATIVA = 'חטיבה'


def parse_year(string: str) -> Year:
    """
    :param string: represents a year
    :return: Year object
    """
    try:
        return YEAR_STRINGS[string.strip()]
    except KeyError:
        raise ValueError(f"can not parse year from {string}")


def parse_semester(string: str) -> Semester:
    """
    :param string: semester description
    :return: a Semester object
    """
    try:
        return SEMESTER_STRINGS[string.strip()]
    except KeyError:
        raise ValueError(f"can not parse semester from {string}")


def parse_course_type(string: str) -> CourseType:
    """
    :param string: course course_type description
    :return: a CourseType object
    """
    try:
        return COURSE_TYPE_STRINGS[string.strip()]
    except KeyError:
        raise ValueError(f"can not parse course course_type from {string}")


def _get_relevant_year():
    """
    if run before august, fetch data for the current year.
     else, fetch next year's data
     """
    now = datetime.now()
    if now.month < 8:
        return now.year
    else:
        return now.year + 1  # next year


def _compose_moon_url(track_id: int,
                      year: int = _get_relevant_year(),
                      faculty: int = 2,  # todo figure out if used
                      entity_id: int = 521,  # todo figure out if used
                      chug_id: int = 521,  # todo figure out if used
                      degree_code: int = 71  # todo figure out if used
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


def parse_course_details(df: pd.DataFrame) -> List[Course]:
    """
    parses a table of course details, given previously-parsed Year and CourseType
    :param df: dataframe of course details
    :return: dataframe of courses
    """
    df.columns = [HEB_ENG_TITLES[title] for title in df.loc[0]]
    df = df.drop(0)
    parsed_courses = []

    df[SEMESTER] = df[SEMESTER].apply(parse_semester)
    df[COURSE_ID] = df[COURSE_ID].astype(int)
    df[HUG_ID] = df[HUG_ID].astype(int)
    df[POINTS] = df[POINTS].astype(float)
    # NOTE fields MAX_YEAR and IS_ELEMENTARY can be parsed as well, heads up for duplicates
    for row in df.T.to_dict().values():
        parsed_courses.append(
            Course(course_id=row[COURSE_ID], name=row[COURSE_NAME], semester=row[SEMESTER],
                   points=row[POINTS], hug_id=row[HUG_ID]))

    return parsed_courses


RE_RANGE = re.compile(r'(\d+(?:\.\d+)?)-(?:\.\d+)?')
RE_MIN = re.compile(r'לפחות\s*(\d+)|(\d+)\s*לפחות')


def parse_track(df: pd.DataFrame) -> Track:
    must = from_list = choice = corner_stones = complementary = hativa = additional_hug = 0
    point_columns = [i for i, c in enumerate(df.columns) if 'כ נקודות' in c]

    for i, r in df.iterrows():
        category = r[0]

        if 'סה\"כ' in category:
            continue

        raw_points = [r[i] for i in point_columns]

        for raw_point in raw_points:
            if not raw_point or pd.isnull(raw_point):  # no need to take Nan or 0 value
                continue

            try:
                points = float(raw_point)

            except ValueError:
                match = RE_RANGE.match(raw_point) or RE_MIN.match(raw_point)
                if match:
                    points = float(match[1] or match[2])  # todo is lower bound the right way?
                else:
                    print(f'could not parse points for category {category}={raw_point}')
                    # todo should we just leave it as is?
                    continue

            if category in (MUST, MUST_IN_HUG, MUST_PROGRAMMING, MUST_SAFETY_LIBRARY) \
                    or MUST in category:
                must += points
            elif category in CHOICE_FROM_LIST or 'במסגרת האשכול' in category:
                from_list += points
            elif category == CHOICE_IN_HUG:
                choice += points
            elif CORNER_STONES in category:
                corner_stones += points
            elif category == COMPLEMENTARY:
                complementary += points
            elif category == HATIVA:
                hativa += points
            elif category == ADDITIONAL_HUG:
                additional_hug += points
            else:
                # print(f'Could not identify {category}={raw_point}, defaulting to MUST')
                must += points

    return Track(must, from_list, choice, complementary, corner_stones, hativa)


def parse_moon(html_body: str, track_number: int = None) -> Tuple[Track,
                                                                  List[Course],
                                                                  List[CourseGroup]]:
    """ parses a page from HUJI-MOON, see _compose_moon_url() """
    df_list = pd.read_html(html_body)

    current_year = current_type = None
    min_points = min_courses = None
    max_courses = None
    track = None

    courses = []
    groups = []

    previous_type = None  # becomes current_type on 'וגם'

    for i, table in enumerate(df_list):
        titles = table.loc[0]
        txt = str(table.iloc[0, 0]).strip()

        if table.shape == (1, 1):  # one-cell table
            if txt in IGNORABLE_TITLES or 'סה"כ' in txt:
                if txt in {'וגם', 'או'}:
                    current_type = previous_type
                continue

            # parse year
            if txt in YEAR_STRINGS:
                current_year = parse_year(txt)
                continue

            # parse course type
            elif txt in COURSE_TYPE_STRINGS:
                current_type = parse_course_type(txt)
                continue

            # parse min points
            min_points_match = MIN_POINTS_PATTERN.search(txt)
            if min_points_match:
                min_points = int(min_points_match.group(1))
                continue

            # parse min courses
            min_course_match = MIN_COURSES_PATTERN.search(txt)
            if min_course_match:
                min_courses = int(min_course_match.group(1))
                continue

            min_one_course_match = MIN_COURSES_ONE_PATTERN.search(txt)
            if min_one_course_match:
                min_courses = 1
                continue

            # parse max group courses
            if MAX_COURSES_ONE_PATTERN.search(txt):
                max_courses = 1
                continue

            # reaching here means txt could not be parsed, could be ok, or a bug

        if any('כ נקודות בחוג' in str(c) for c in table.columns):
            if track is not None:
                raise ValueError("found two track_number-detail tables on the same page")
            try:
                track = parse_track(table)
            except NotImplementedError as e:
                print(f'#{track_number}')
                raise e

        if COURSE_DETAILS_TITLES.issubset(titles):
            if not all((current_year, current_type)):
                raise ValueError("reached course details before parsing "
                                 f"current year/course course_type, track#={track_number}")
            # noinspection PyTypeChecker
            temp_courses = parse_course_details(table)
            if not temp_courses:
                continue

            courses.extend(temp_courses)

            ids = [c.id for c in temp_courses]
            temp_group = CourseGroup(track_number, ids, current_type, min_courses, min_points)
            groups.append(temp_group)

            previous_type = current_type
            min_courses = min_points = current_type = None
        else:
            if 'לכל היותר' in txt and not max_courses:
                raise NotImplementedError("todo implement parsing of max_courses>1")
    if track:
        track.groups = groups

    return track, courses, groups
