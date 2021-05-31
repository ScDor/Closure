import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Closure_Project.settings")

import django

django.setup()

from rest_api.models import Student, CourseGroup, CourseType

REQUIRED_COURSE_TYPES = (CourseType.MUST, CourseType.FROM_LIST, CourseType.CHOICE)  # order matters! do not modify
ALL_COURSE_TYPES = REQUIRED_COURSE_TYPES + ('CORNER_STONE', 'COMPLEMENTARY')


def remaining(student: Student):
    track = student.track
    groups = CourseGroup.objects.filter(track=track)

    required_by_type = {k: set() for k in REQUIRED_COURSE_TYPES}
    required_courses = set()

    for group in groups:
        group_courses = list(group.courses.all())

        required_by_type[group.course_type].update(group_courses)
        required_courses.update(group_courses)

    done = {t: 0 for t in ALL_COURSE_TYPES}

    for course in student.courses.all():
        if course.is_corner_stone:
            done['CORNER_STONE'] += course.points

        elif course in required_courses:
            for course_type in REQUIRED_COURSE_TYPES:  # ordered by importance
                if course in required_by_type[course_type]:
                    done[course_type] += course.points
                    break  # prevents courses from being counted in more than one type

        else:
            done['COMPLEMENTARY'] += course.points

    result = [{'type': CourseType.MUST.name, 'required': track.points_must, 'done': done[CourseType.MUST]},
              {'type': CourseType.FROM_LIST.name, 'required': track.points_from_list,
               'done': done[CourseType.FROM_LIST]},
              {'type': CourseType.CHOICE.name, 'required': track.points_choice, 'done': done[CourseType.CHOICE]},
              {'type': 'CORNER_STONE', 'required': track.points_corner_stones, 'done': done['CORNER_STONE']},
              {'type': 'COMPLEMENTARY', 'required': track.points_complementary, 'done': done['COMPLEMENTARY']}]
    return result
