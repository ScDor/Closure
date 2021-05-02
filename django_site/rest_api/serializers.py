from rest_framework import serializers

from .models import Course, Student, CourseGroup


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'semester',
                  'points', 'hug_id')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'track', 'name', 'year')


class CourseGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('name', 'track', 'courses',
                  'course_type', 'required_course_count', 'required_points')
