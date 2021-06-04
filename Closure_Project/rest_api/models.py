# Create your models here.
import uuid
from enum import Enum

from django.contrib.auth.models import User
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
    name = models.CharField(max_length=20)
    semester = models.CharField(max_length=6, choices=Semester.choices)
    is_given_this_year = models.BooleanField()
    points = models.FloatField()
    is_corner_stone = models.BooleanField(null=True)
    comment = models.CharField(max_length=255, blank=True)

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
    name = models.CharField(max_length=255)
    points_must = models.IntegerField()
    points_from_list = models.IntegerField()
    points_choice = models.IntegerField()
    points_complementary = models.IntegerField()
    points_corner_stones = models.IntegerField()
    points_minor = models.IntegerField()
    points_additional_hug = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["track_number", "data_year"], name="track_year")]

    def __str__(self):
        return f'#{self.track_number} {self.name} ({self.data_year})'

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
    course_type = models.CharField(max_length=20, choices=CourseType.choices)
    year_in_studies = models.IntegerField()
    index_in_track_year = models.IntegerField()
    required_course_count = models.IntegerField(null=True)
    required_points = models.IntegerField(null=True)
    comment = models.CharField(max_length=255, null=True)
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


REQUIRED_COURSE_TYPES = (CourseType.MUST, CourseType.FROM_LIST, CourseType.CHOICE)  # order matters! do not modify
ALL_COURSE_TYPES = REQUIRED_COURSE_TYPES + ('CORNER_STONE', 'COMPLEMENTARY')


class Student(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    year_in_studies = models.IntegerField(choices=Year.choices)
    courses = models.ManyToManyField(Course, through='Take', blank=True)

    def __str__(self):
        return ', '.join((self.name.title(),
                          f'year={self.year_in_studies}',
                          f'track={self.track.track_number}',
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
            if course in counted:
                continue
            counted.add(course)

            if course.is_corner_stone:
                done[CourseType.CORNER_STONE] += course.points

            elif course in required_courses:
                for course_type in REQUIRED_COURSE_TYPES:  # ordered by importance
                    if course in required_by_type[course_type]:
                        done[course_type] += course.points
                        break  # prevents courses from being counted in more than one type

            else:
                done[CourseType.SUPPLEMENTARY] += course.points

        result = {CourseType.MUST.name:
                      {'required': track.points_must,
                       'done': done[CourseType.MUST]},

                  CourseType.FROM_LIST.name:
                      {'required': track.points_from_list,
                       'done': done[CourseType.FROM_LIST]},

                  CourseType.CHOICE.name:
                      {'required': track.points_choice,
                       'done': done[CourseType.CHOICE]},

                  CourseType.CORNER_STONE.name:
                      {'required': track.points_corner_stones,
                       'done': done[CourseType.CORNER_STONE]},

                  CourseType.SUPPLEMENTARY.name:
                      {'required': track.points_complementary,
                       'done': done[CourseType.SUPPLEMENTARY]}}

        return result


class Take(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_1')
    year_in_studies = models.IntegerField(choices=Year.choices)
    semester = models.CharField(choices=Semester.choices, max_length=10)

    def __str__(self):
        return ', '.join((f'{self.course.course_id}',
                          f'year={self.year_in_studies}',
                          f'semester={self.semester.lower()}'))

    @property
    def type(self) -> CourseType:
        if self.course.is_corner_stone:
            return CourseType.CORNER_STONE

        cg_set = self.student.track.coursegroup_set
        matching_cg = cg_set.filter(courses__id=self.course.id).all()
        types = {cg.course_type for cg in matching_cg}
        for course_type in [CourseType.MUST, CourseType.FROM_LIST, CourseType.CHOICE]:
            if course_type in types:
                return course_type

        return CourseType.SUPPLEMENTARY
