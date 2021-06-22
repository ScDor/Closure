import django
import pytest
import os

from rest_api import models

@pytest.mark.django_db
def test_can_create_course():
    course = models.Course.objects.create(course_id=67778, data_year=2020, name="Software Testing",
                                          is_given_this_year=True, points=2, is_corner_stone=False)

    course.save()

    course2 = models.Course.objects.get(course_id=67778)
    assert course2.name == "Software Testing"