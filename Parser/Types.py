from enum import Enum


class Year(Enum):
    """ year in studies """
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7


class Semester(Enum):
    """ semester when the course is given """
    A = 'A'
    B = 'B'
    SUMMER = 'Summer'
    EITHER = 'Either'
    ANNUAL = 'Annual'


class CourseType(Enum):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 'Must'
    CHOICE = 'Choice'
    FROM_LIST = 'Choose From List'


class Course:
    id: int
    year: Year
    name: str
    course_type: CourseType
    semester: Semester
    points: float
    hug_id: int
    max_year: int = None
    is_elementary: bool = None

    def __init__(self, course_id: int, year: Year, name: str, course_type: CourseType,
                 semester: Semester, points: float, hug_id: int, max_year: int = None,
                 is_elementary: bool = None):
        self.id = course_id
        self.year = year
        self.name = name
        self.course_type = course_type
        self.semester = semester
        self.points = points
        self.hug_id = hug_id
        self.max_year = max_year
        self.is_elementary = is_elementary

    def __repr__(self):
        return f'#{self.id}, ' \
               f'{self.points}pts, ' \
               f'{self.course_type.name},' \
               f'{self.year}, ' \
               f'{self.semester.name}'
