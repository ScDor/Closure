from enum import Enum
from typing import Union, List


class Faculty(Enum):
    SOCIAL = 1
    SCIENCE = 2
    LAW = 3
    BUSINESS_MANAGEMENT = 6
    SPIRIT = 7
    CSE = 12
    AGRICULTURE = 30
    MEDICINE = 99

    def __str__(self):
        return f'{self.name.title()} Year'


class Semester(Enum):
    """ semester when the course is given """
    A = 'FIRST'
    B = 'SECOND'
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
    def __init__(self, course_id: int, name: str, semester: Semester, points: float,
                 hug_id: int, is_given_this_year: bool, data_year: int):
        self.id = course_id
        self.name = name
        self.semester = semester
        self.data_year = data_year
        self.points = points
        self.hug_id = hug_id
        self.is_given_this_year = is_given_this_year

    def __repr__(self):
        return ', '.join((str(self.id),
                          f'{self.points}pts',
                          str(self.semester)))


class CourseGroup:
    def __init__(self,
                 track_id: int,
                 courses: List[int],
                 course_type: CourseType,
                 year: int,
                 data_year: int,
                 index_in_track_year: int,
                 required_course_count: Union[int, None],
                 required_points: Union[int, None],
                 comment: Union[str, None] = None,
                 ):
        self.track = track_id
        self.course_ids = courses
        self.type = course_type
        self.year = year
        self.data_year = data_year
        self.index_in_track_year = index_in_track_year

        if course_type == CourseType.MUST \
                and required_course_count is None \
                and required_points is None:
            required_course_count = len(courses)

        self.required_course_count = required_course_count
        self.required_points = required_points
        self.comment = comment

    def __repr__(self):
        if self.required_course_count:
            if self.required_course_count == len(self.course_ids):
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
                         *(str(c) for c in self.course_ids)))


class Track:
    def __init__(self,
                 track_id: int,
                 track_name: str,
                 track_comment: str,
                 data_year: int,
                 points_must: int = 0,
                 points_from_list: int = 0,
                 points_choice: int = 0,
                 points_complementary: int = 0,
                 points_corner_stones: int = 0,
                 points_minor: int = 0,
                 additional_hug: int = 0,
                 groups: List[CourseGroup] = None):
        self.id = track_id
        self.name = track_name
        self.comment = track_comment
        self.data_year = data_year
        self.points_must = points_must
        self.points_from_list = points_from_list
        self.points_choice = points_choice
        self.points_complementary = points_complementary
        self.points_corner_stones = points_corner_stones
        self.points_minor = points_minor
        self.points_additional_hug = additional_hug

        self.groups = groups

    def __repr__(self):
        value_dictionary = {}

        for (name, value) in ('id', self.id,
                              ('name', self.name),
                              ('must', self.points_must),
                              ('from_list', self.points_from_list),
                              ('choice', self.points_choice),
                              ('complementary', self.points_complementary),
                              ('corner_stones', self.points_corner_stones),
                              ('points_minor', self.points_minor),
                              ('additional_hug', self.points_additional_hug),
                              ('groups', self.groups)):
            if value:
                value_dictionary[name] = value

        return str(value_dictionary)
