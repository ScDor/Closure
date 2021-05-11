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


class Semester(models.TextChoices):
    """ semester when the course is given """
    A = 'FIRST'
    B = 'SECOND'
    SUMMER = 'Summer'
    EITHER = 'Either'
    ANNUAL = 'Annual'

    def __str__(self):
        return f'Semester {self.name}'


class CourseType(models.TextChoices):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 'Must'
    CHOICE = 'Choice'
    FROM_LIST = 'Choose From List'


class Course(models.Model):
    course_id = models.IntegerField()
    year = models.IntegerField()
    name = models.CharField(max_length=20)
    semester = models.CharField(max_length=6, choices=Semester.choices)
    is_given_this_year = models.BooleanField()
    points = models.FloatField()
    hug_id = models.IntegerField()

    class Meta:
        unique_together = ('course_id', 'year', 'hug_id')


    def __repr__(self):
        return ', '.join((str(self.course_id),
                          f'{self.points}pts',
                          str(self.semester)))


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track = models.IntegerField()
    year = models.IntegerField()
    name = models.CharField(max_length=255)
    points_must = models.IntegerField()
    points_from_list = models.IntegerField()
    points_choice = models.IntegerField()
    points_complementary = models.IntegerField()
    points_corner_stones = models.IntegerField()
    points_minor = models.IntegerField()
    points_additional_hug = models.IntegerField()
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["track", "year"], name="track_year")]

    def __repr__(self):
        value_dictionary = {}

        for (name, value) in (('must', self.points_must),
                              ('from_list', self.points_from_list),
                              ('choice', self.points_choice),
                              ('complementary', self.points_complementary),
                              ('corner_stones', self.points_corner_stones),
                              ('points_minor', self.points_minor),
                              ('additional_hug', self.points_additional_hug)):
            if value:
                value_dictionary[name] = value

        return str(value_dictionary)


class CourseGroup(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=20, choices=CourseType.choices)
    year_in_studies = models.IntegerField()
    index_in_track_year = models.IntegerField()
    courses = models.ManyToManyField(Course)
    required_course_count = models.IntegerField(null=True)
    required_points = models.IntegerField(null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["track", "year_in_studies", 'course_type', 'index_in_track_year'],
                                    name="group_unique")]


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    year_in_studies = models.IntegerField(choices=Year.choices)
    courses = models.ManyToManyField(Course)