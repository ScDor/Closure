from enum import Enum
from typing import Union, List


class Year(Enum):
    """ year in studies """
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7

    def __str__(self):
        return f'Year {self.name}'


class Semester(Enum):
    """ semester when the course is given """
    A = 'A'
    B = 'B'
    SUMMER = 'Summer'
    EITHER = 'Either'
    ANNUAL = 'Annual'

    def __str__(self):
        return f'Semester {self.name}'


class CourseType(Enum):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 'Must'
    CHOICE = 'Choice'
    FROM_LIST = 'Choose From List'


class Course:
    def __init__(self, course_id: int, name: str, semester: Semester,
                 points: float, hug_id: int, max_year: int = None, is_elementary: bool = None):
        self.id = course_id
        self.name = name
        self.semester = semester
        self.points = points
        self.hug_id = hug_id
        self.max_year = max_year
        self.is_elementary = is_elementary

    def __repr__(self):
        return ', '.join((str(self.id),
                          f'{self.points}pts',
                          str(self.semester)))


class CourseGroup:
    def __init__(self,
                 track: int,
                 courses: List[int],
                 course_type: CourseType,
                 required_course_count: Union[int, None],
                 required_points: Union[int, None]
                 ):
        self.track = track
        self.type = course_type

        if course_type == CourseType.MUST and \
                required_course_count is None and required_points is None:
            required_course_count = len(courses)

        self.required_course_count = required_course_count
        self.required_points = required_points

        if not courses:
            raise ValueError("can not create group without courses")

        self.courses = courses

    def __repr__(self):
        if self.required_course_count:
            if self.required_course_count == len(self.courses):
                requirement = 'must do all'
            else:
                requirement = f'need {self.required_course_count} courses'
        elif self.required_points:
            requirement = f'need {self.required_points} points'
        else:
            requirement = 'no requirements'

        return ','.join((str(self.track),
                         str(self.type),
                         requirement,
                         *(str(c) for c in self.courses)))
