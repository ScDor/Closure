from rest_framework import serializers

from .models import Course, Student, CourseGroup


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'track', 'name',
                  'semester', 'year', 'type',
                  'points', 'hug_id')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'group', 'courses')


class CourseGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('track', 'type', 'required_course_count',
                  'required_points', 'courses')
