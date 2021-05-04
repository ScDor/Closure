# Create your models here.
import uuid
from enum import Enum

from django.db import models


class Faculty(Enum):
    SOCIAL = 1
    SCIENCE = 2
    LAW = 3
    BUSINESS_MANAGEMENT = 6
    SPIRIT = 7
    CSE = 12
    AGRICULTURE = 30
    MEDICINE = 99


class Year(models.IntegerChoices):
    """ year in studies """
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7

    def __str__(self):
        return f'{self.name.title()} Year'


class Semester(models.IntegerChoices):
    """ semester when the course is given """
    A = 1, 'FIRST'
    B = 2, 'SECOND'
    SUMMER = 3, 'Summer'
    EITHER = 4, 'Either'
    ANNUAL = 5, 'Annual'

    def __str__(self):
        return f'Semester {self.name}'


class CourseType(models.IntegerChoices):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 1, 'Must'
    CHOICE = 2, 'Choice'
    FROM_LIST = 3, 'Choose From List'


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    semester = models.IntegerField(choices=Semester.choices)
    points = models.FloatField()
    hug_id = models.IntegerField()
    is_given_this_year = models.BooleanField()

    def __repr__(self):
        return ', '.join((str(self.id),
                          f'{self.points}pts',
                          str(self.semester)))


class Track(models.Model):
    track_number = models.IntegerField(primary_key=True)
    points_must = models.IntegerField()
    points_from_list = models.IntegerField()
    points_choice = models.IntegerField()
    complementary = models.IntegerField()
    corner_stones = models.IntegerField()
    points_minor = models.IntegerField()
    points_additional_hug = models.IntegerField()

    # def __init__(self, must: int = 0, from_list: int = 0, points_choice: int = 0,
    #              complementary: int = 0, corner_stones: int = 0, points_minor: int = 0,
    #              additional_hug: int = 0, groups: List[CourseGroup] = None):
    #
    #     self.points_must = must
    #     self.points_from_list = from_list
    #     self.points_choice = points_choice
    #     self.complementary = complementary
    #     self.corner_stones = corner_stones
    #     self.points_minor = points_minor
    #     self.points_additional_hug = additional_hug
    #
    #     self.groups = groups

    def __repr__(self):
        value_dictionary = {}

        for (name, value) in (('must', self.points_must),
                              ('from_list', self.points_from_list),
                              ('choice', self.points_choice),
                              ('complementary', self.complementary),
                              ('corner_stones', self.corner_stones),
                              ('points_minor', self.points_minor),
                              ('additional_hug', self.points_additional_hug)):
            if value:
                value_dictionary[name] = value

        return str(value_dictionary)


class CourseGroup(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    course_type = models.IntegerField(choices=CourseType.choices)
    required_course_count = models.IntegerField()
    required_points = models.IntegerField()


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    year = models.IntegerField(choices=Year.choices)
    courses = models.ManyToManyField(Course)
