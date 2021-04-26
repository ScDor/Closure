# Create your models here.
import uuid

from django.db import models


class Year(models.IntegerChoices):
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


class Semester(models.TextChoices):
    """ semester when the course is given """
    A = 'A'
    B = 'B'
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
    id = models.DecimalField(primary_key=True)
    track = models.ForeignKey('CourseGroup', on_delete=models.CASCADE)
    name = models.CharField()
    semester = models.CharField(choices=Semester.choices)
    year = models.IntegerField(choices=Year)
    type = models.CharField(choices=CourseType)
    points = models.FloatField()
    hug_id = models.IntegerField()

    def __repr__(self):
        return ', '.join((str(self.id),
                          f'{self.points}pts',
                          str(self.semester)))


class CourseGroup(models.Model):
    track = models.IntegerField(primary_key=True)
    type = models.CharField(choices=CourseType.choices)
    required_course_count = models.IntegerField()
    required_points = models.IntegerField()
    courses = models.ManyToManyField(Course)


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    # def __repr__(self):
    #     if self.required_course_count:
    #         if self.required_course_count == len(self.courses):
    #             requirement = 'must do all'
    #         else:
    #             requirement = f'need {self.required_course_count} courses'
    #     elif self.required_points:
    #         requirement = f'need {self.required_points} points'
    #     else:
    #         requirement = 'no requirements'
    #
    #     return ','.join((str(self.track),
    #                      str(self.type),
    #                      requirement,
    #                      *(str(c) for c in self.courses)))
