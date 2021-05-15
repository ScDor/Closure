import os
from typing import Dict, List

import requests
import json

import pandas as pd

url = 'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?faculty=2&year=2021&courseId=67109'


def construct_course_details(course_id: int, faculty: int = 2, year: int = 2021) -> str:
    return f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?faculty={faculty}&year={year}&courseId={course_id}'


# r = requests.get(url).text
# with open('crs.json', 'w', encoding='utf8') as f:
#     json.dump(r, f)
#
# with open('crs.json', 'r', encoding='utf8') as f:
#     html_body = json.load(f)


def _parse_requirement_table(table: pd.DataFrame, current_course_id: int) -> List[Dict[str, int]]:
    """
    parses course id and min_grades of a requirement table
    """
    return [{'course_id': row[1][0], 'min_grade': row[1][4]} for row in table.T.items()
            if int(row[1][0]) != current_course_id]  # did you know 67101 is prerequisite to 67101? 🤦


def parse_requirements(html_body: str, current_course_id: int) -> List[List[Dict[str, int]]]:
    if 'tblGroupsCourseLev\"' not in html_body:
        return []

    titles = [row[0][0] for row in pd.read_html(html_body, attrs={'id': 'tblGroupsCourseLev'})]

    parsed_requirements = []

    for i in range(len(titles)):
        try:
            df_list = pd.read_html(html_body, attrs={'id': f'lstGroupsCourseLev_grdCourses_{i}'})

            # an empty df_list indicates a title without following courses, that's fine and is ignored.
            parsed_requirements.append(_parse_requirement_table(df_list[0], current_course_id) if df_list else [])

        except ValueError as e:
            if str(e) == 'No tables found':
                break
            else:
                raise e

    assert len(parsed_requirements) == len(titles)
    return parsed_requirements



