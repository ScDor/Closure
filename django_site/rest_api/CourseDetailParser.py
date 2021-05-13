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


def _parse_requirement_table(table: pd.DataFrame):
    return [{'course_id': row[1][0], 'min_grade': row[1][4]} for row in table.T.items()]


def parse_requirements(html_body: str):
    titles = [row[0][0] for row in pd.read_html(html_body, attrs={'id': 'tblGroupsCourseLev'})]
    requirements = []

    for i in range(len(titles)):
        try:
            df_list = pd.read_html(html_body, attrs={'id': f'lstGroupsCourseLev_grdCourses_{i}'})

            # an empty df_list indicates a title without following courses, that's fine and is ignored.
            requirements.append(_parse_requirement_table(df_list[0]) if df_list else [])

        except ValueError as e:
            if str(e) == 'No tables found':
                break
            else:
                raise e

    assert len(requirements) == len(titles)
    return list(zip(titles, requirements))


