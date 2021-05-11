from rest_framework import serializers

from .models import Track, Course, Student, CourseGroup


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'year', 'name', 'semester',
                  'points', 'is_given_this_year', 'hug_id')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'track', 'name', 'year_in_studies', 'courses')


class CourseGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('track', 'year', 'course_type', 'year_in_studies',
                  'index_in_track_year',
                  'courses', 'required_course_count', 'required_points',
                  'comment')


class TrackGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('track', 'year', 'points_must', 'points_from_list',
                  'points_choice', 'points_complementary', 'points_corner_stones',
                  'points_minor', 'points_additional_hug', 'comment')
