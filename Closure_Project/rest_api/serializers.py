from rest_framework import serializers

from .models import Track, Course, Student, CourseGroup, Take, Hug


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id', 'data_year', 'name', 'semester', 'points', 'is_given_this_year',
                  'is_corner_stone', 'comment')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'track', 'name', 'year_in_studies', 'courses')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('track_number', 'name', 'data_year', 'points_must', 'points_from_list',
                  'points_choice', 'points_complementary', 'points_corner_stones',
                  'points_minor', 'points_additional_hug',  'comment')


class TakeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Take
        fields = ('student', 'course', 'year_in_studies', 'semester')


class CourseGroupSerializer(serializers.HyperlinkedModelSerializer):
    courses = TakeSerializer(source='take_set', many=True)

    class Meta:
        model = CourseGroup
        fields = ('track', 'course_type', 'year_in_studies', 'index_in_track_year', 'courses',
                  'required_course_count', 'required_points','comment')


class HugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hug
        fields = ('course',)
