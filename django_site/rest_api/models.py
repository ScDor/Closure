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


class Semester(models.IntegerChoices):
    """ semester when the course is given """
    A = 1
    B = 2
    SUMMER = 3
    EITHER = 4
    ANNUAL = 5

    def __str__(self):
        return f'Semester {self.name}'


class CourseType(models.IntegerChoices):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 1
    CHOICE = 2
    FROM_LIST = 3


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    track = models.ForeignKey('CourseGroup', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    semester = models.IntegerField(choices=Semester.choices)
    year = models.IntegerField(choices=Year.choices)
    type = models.IntegerField(choices=CourseType.choices)
    points = models.IntegerField()
    hug_id = models.IntegerField()

    def __repr__(self):
        return ', '.join((str(self.id),
                          f'{self.points}pts',
                          str(self.semester)))


class CourseGroup(models.Model):
    track = models.IntegerField(primary_key=True)
    type = models.IntegerField(choices=CourseType.choices)
    required_course_count = models.IntegerField()
    required_points = models.IntegerField()
    courses = models.ManyToManyField(Course)


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
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
