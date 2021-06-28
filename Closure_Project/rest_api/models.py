# Create your models here.
import uuid
from enum import Enum

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Case, When


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
    SUMMER = 'SUMMER'
    EITHER = 'EITHER'
    ANNUAL = 'ANNUAL'

    def __str__(self):
        return f'{self.value.title()} Semester'


class CourseType(models.TextChoices):
    """ course course_type: must take, must choose from a list or free choice """
    MUST = 'MUST'
    CHOICE = 'CHOICE'
    FROM_LIST = 'CHOOSE_FROM_LIST'
    CORNER_STONE = 'CORNER_STONE'
    SUPPLEMENTARY = 'SUPPLEMENTARY'


class Course(models.Model):
    course_id = models.IntegerField()
    data_year = models.IntegerField()
    name = models.TextField()
    semester = models.TextField(choices=Semester.choices)
    is_given_this_year = models.BooleanField()
    points = models.FloatField()
    is_corner_stone = models.BooleanField(null=True)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('course_id', 'data_year')

    def __str__(self):
        return ', '.join((str(self.course_id),
                          f'{self.points}pts',
                          str(self.semester)))


class Hug(models.Model):
    id = models.IntegerField(primary_key=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        courses = ','.join(self.courses.all())
        return f'{self.id}: {courses}'


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_number = models.IntegerField()
    data_year = models.IntegerField()
    name = models.TextField()
    points_must = models.IntegerField()
    points_from_list = models.IntegerField()
    points_choice = models.IntegerField()
    points_complementary = models.IntegerField()
    points_corner_stones = models.IntegerField()
    points_minor = models.IntegerField()
    points_additional_hug = models.IntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["track_number", "data_year"], name="track_year")]

    def __str__(self):
        return f'{self.track_number} {self.name} ({self.data_year})'

    def courses(self):
        courses = []

        # get the coursegroups and sort by course type
        order = Case(*[When(course_type=course_type, then=pos) for pos, course_type in enumerate(ALL_COURSE_TYPES)])
        cgs = self.coursegroup_set.order_by(order).all()

        # append all the course ids to a list
        for cg in cgs:
            for course in cg.courses.all():
                courses.append(course.id)
        return courses

    @property
    def total_points(self) -> int:
        return self.points_must \
               + self.points_from_list \
               + self.points_choice \
               + self.points_complementary \
               + self.points_corner_stones \
               + self.points_minor \
               + self.points_additional_hug

    def describe(self):
        value_dictionary = {}

        for (name, value) in (('track_name', self.name),
                              ('track_id', self.points_must),
                              ('must', self.points_must),
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
    course_type = models.TextField(choices=CourseType.choices)
    year_in_studies = models.IntegerField(choices=Year.choices)
    index_in_track_year = models.IntegerField()
    required_course_count = models.IntegerField(null=True)
    required_points = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    courses = models.ManyToManyField(Course)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['track', 'year_in_studies', 'course_type', 'index_in_track_year'],
                name='group_unique')]

    def __str__(self):
        if self.required_course_count:
            if self.required_course_count == self.courses.count():
                requirement = 'must do all'
            else:
                requirement = f'need {self.required_course_count} courses'
        elif self.required_points:
            requirement = f'need {self.required_points} points'
        else:
            requirement = 'no requirements'

        return ','.join((str(self.track),
                         str(self.course_type),
                         requirement,
                         *(str(c) for c in self.courses.all())))


REQUIRED_COURSE_TYPES = (
    CourseType.MUST, CourseType.FROM_LIST, CourseType.CHOICE)  # order matters! do not modify
ALL_COURSE_TYPES = REQUIRED_COURSE_TYPES + (CourseType.CORNER_STONE, CourseType.SUPPLEMENTARY)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    year_in_studies = models.IntegerField(choices=Year.choices, null=True)
    courses = models.ManyToManyField(Course, through='Take', blank=True)

    def __str__(self):
        return ', '.join((self.user.username,
                          self.user.get_full_name(),
                          f'year={self.year_in_studies}',
                          f'track={self.track.track_number}' if self.track else 'לא הוגדר מסלול',
                          f'took {len(self.courses.all())} courses'))

    @property
    def remaining(self):
        track = self.track
        groups = track.coursegroup_set.all()
        required_by_type = {k: set() for k in REQUIRED_COURSE_TYPES}
        required_courses = set()

        for group in groups:
            group_courses = list(group.courses.all())

            required_by_type[group.course_type].update(group_courses)
            required_courses.update(group_courses)

        done = {t: 0 for t in ALL_COURSE_TYPES}
        counted = set()

        for take in self.take_set.all():
            course = take.course
            if course not in counted:
                counted.add(course)
                done[take.type] += course.points

        result = {CourseType.MUST.name: {'required': track.points_must,
                                         'done': done[CourseType.MUST]},

                  CourseType.FROM_LIST.name: {'required': track.points_from_list,
                                              'done': done[CourseType.FROM_LIST]},

                  CourseType.CHOICE.name: {'required': track.points_choice,
                                           'done': done[CourseType.CHOICE]},

                  CourseType.CORNER_STONE.name: {'required': track.points_corner_stones,
                                                 'done': done[CourseType.CORNER_STONE]},

                  CourseType.SUPPLEMENTARY.name: {'required': track.points_complementary,
                                                  'done': done[CourseType.SUPPLEMENTARY]}}

        def trickle_down(trickle_from: CourseType, trickle_to: CourseType) -> None:
            """
            moves extra points between groups, for example, a student taking too many
            FROM_LIST courses will have those points counted as CHOICE instead.

            :param trickle_from: category from which points are moved
            :param trickle_to:category to which points are moved
            :return: None
            """
            extra = result[trickle_from.name]['done'] - result[trickle_from.name]['required']
            if extra > 0:
                result[trickle_from.name]['done'] -= extra
                result[trickle_to.name]['done'] += extra

        trickle_down(CourseType.MUST, CourseType.CHOICE)
        trickle_down(CourseType.FROM_LIST, CourseType.CHOICE)
        trickle_down(CourseType.CHOICE, CourseType.SUPPLEMENTARY)
        trickle_down(CourseType.CORNER_STONE, CourseType.SUPPLEMENTARY)

        return result


class Take(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_in_studies = models.IntegerField(choices=Year.choices)
    semester = models.TextField(choices=Semester.choices)

    def __str__(self):
        return ', '.join((f'{self.course.course_id}',
                          f'year={self.year_in_studies}',
                          f'semester={self.semester.lower()}'))

    @property
    def type(self) -> CourseType:
        from rest_api.rest_utils import get_course_type
        return get_course_type(self.student.track, self.course)
