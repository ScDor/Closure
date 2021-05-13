import os
import re
from datetime import datetime
from typing import List, Tuple, Optional

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.django_site.settings")

import django

django.setup()

import pandas as pd
from bs4 import BeautifulSoup

from .models import Semester, CourseType, Course, CourseGroup, Track

TRACK_NAME_PATTERN = re.compile(r'מסלול\s+(.+)\(\d{4}\)')
MIN_POINTS_PATTERN = re.compile(r'לפחות\s*(\d+)\s*נ')
MIN_COURSES_PATTERN = re.compile(r'יש ללמוד.*(\d+) מתוך רשימת קורסים')
MIN_COURSES_ONE_PATTERN = re.compile(r'לפחות קורס 1\s|את אחד')
MAX_COURSES_ONE_PATTERN = re.compile(r'אחד לכל היותר|רק קורס 1')

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
    'שנה א\'': 1,
    'שנה ב\'': 2,
    'שנה ג\'': 3,
    'שנה ד\'': 4,
    'שנה ה\'': 5,
    'שנה ו\'': 6,
    'שנה ז\'': 7
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
    'או'
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
MINOR = 'חטיבה'


def parse_track_name(soup: BeautifulSoup) -> str:
    """
    :param soup: BeautifulSoup object of the html page
    :return: track name
    """
    title = soup.find('span', {'id': 'lblMaslulName'}).text
    return re.match(TRACK_NAME_PATTERN, title).group(1).strip()


def parse_track_comment(soup: BeautifulSoup) -> str:
    """
    :param soup: BeautifulSoup object of the html page
    :return: track comment
    """
    label = soup.find('lblDescription')
    if label:
        return label.text.strip()


def parse_year(string: str) -> int:
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


NOT_GIVEN_THIS_YEAR = '(לא נלמד השנה)'


def parse_course_details(df: pd.DataFrame, data_year: int) -> List[Course]:
    """
    parses a table of course details, given previously-parsed Year and CourseType
    :param df: dataframe of course details
    :param data_year: year to which this course is relevant (shnaton year)
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
        is_given = NOT_GIVEN_THIS_YEAR not in row[COURSE_NAME]
        name = row[COURSE_NAME].replace(NOT_GIVEN_THIS_YEAR, "")

        parsed_courses.append(
            Course.objects.update_or_create(course_id=row[COURSE_ID],
                                            year=data_year,
                                            name=name,
                                            semester=row[SEMESTER],
                                            is_given_this_year=is_given,
                                            points=row[POINTS],
                                            hug_id=row[HUG_ID],
                                            )[0])

    return parsed_courses


RE_RANGE = re.compile(r'(\d+(?:\.\d+)?)-(?:\.\d+)?')
RE_MIN = re.compile(r'לפחות\s*(\d+)|(\d+)\s*לפחות')


def parse_track(df: pd.DataFrame, track_id: int, track_name: str, track_comment: str,
                data_year: int) -> Track:
    must = from_list = choice = corner_stones = complementary = minor = additional_hug = 0
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
            elif category == MINOR:
                minor += points
            elif category == ADDITIONAL_HUG:
                additional_hug += points
            else:
                # print(f'Could not identify {category}={raw_point}, defaulting to MUST')
                must += points
    return Track.objects.update_or_create(track=track_id,
                                          year=data_year,
                                          name=track_name,
                                          points_must=must,
                                          points_from_list=from_list,
                                          points_choice=choice,
                                          points_complementary=complementary,
                                          points_corner_stones=corner_stones,
                                          points_minor=minor,
                                          points_additional_hug=additional_hug,
                                          comment=track_comment)[0]


def parse_moon(html_body: str, track_id: int, data_year: int) -> Optional[Tuple[Track,
                                                                                List[Course],
                                                                                List[CourseGroup]]]:
    """ parses a page from HUJI-MOON, see _compose_moon_url() """
    soup = BeautifulSoup(html_body, 'html.parser')

    track_name = parse_track_name(soup)
    track_comment = parse_track_comment(soup)

    df_list = pd.read_html(html_body)

    current_year = current_type = None
    min_points = min_courses = None
    max_courses = None
    track = None
    index_in_track_year = 0

    courses = []
    groups = []

    current_comment = None
    previous_type = None  # becomes current_type on 'וגם'

    # parse track first
    for table in reversed(df_list):
        if any('כ נקודות בחוג' in str(c) for c in table.columns):
            # if track is not None:
            #     raise ValueError("found two track_number-detail tables on the same page")
            try:
                track = parse_track(table, track_id, track_name, track_comment, data_year)
                break
            except NotImplementedError as e:
                print(f'#{track_id}')
                raise e
    if track is None:
        return
    for i, table in enumerate(df_list):
        titles = table.loc[0]
        txt = str(table.iloc[0, 0]).strip()

        if table.shape == (1, 1):  # one-cell table
            if txt in IGNORABLE_TITLES or 'סה"כ' in txt:
                if txt in {'וגם', 'או'}:  # todo handle alternatives
                    current_type = previous_type
                continue

            # parse year
            if txt in YEAR_STRINGS:
                year = parse_year(txt)
                if current_year and (year != current_year):
                    index_in_track_year = 0
                current_year = year
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

            else:
                if 'מספר הקורסשם הקורס' not in txt:
                    current_comment = txt

        # if any('כ נקודות בחוג' in str(c) for c in table.columns):
        #     if track is not None:
        #         raise ValueError("found two track_number-detail tables on the same page")
        #     try:
        #         track = parse_track(table, track_id, track_name, track_comment, data_year)
        #     except NotImplementedError as e:
        #         print(f'#{track_id}')
        #         raise e

        if COURSE_DETAILS_TITLES.issubset(titles):
            if not all((current_year, current_type)):
                raise ValueError("reached course details before parsing "
                                 f"current year/course course_type, track#={track_id}")
            # noinspection PyTypeChecker
            temp_courses = parse_course_details(table, data_year)
            if not temp_courses:
                continue
            # Course.objects.bulk_update(temp_courses)
            courses.extend(temp_courses)

            # ids = [c.course_id for c in temp_courses]
            # track = Track.objects.get(track=track_id, year=data_year)
            if current_type == CourseType.MUST \
                    and min_courses is None \
                    and min_points is None:
                min_courses = len(courses)
            temp_group, _ = CourseGroup.objects.update_or_create(track=track,
                                                                 course_type=current_type,
                                                                 year_in_studies=current_year,
                                                                 index_in_track_year=index_in_track_year,
                                                                 required_course_count=min_courses,
                                                                 required_points=min_points,
                                                                 comment=current_comment,
                                                                 )
            for course in temp_courses:
                temp_group.courses.add(course)
            current_comment = None
            groups.append(temp_group)
            index_in_track_year += 1

            previous_type = current_type
            min_courses = min_points = current_type = None
        else:
            if 'לכל היותר' in txt and not max_courses:
                raise NotImplementedError("todo implement parsing of max_courses>1")
    # if track:
    #     track.groups = groups

    return track, courses, groups
