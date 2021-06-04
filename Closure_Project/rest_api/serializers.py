import logging

from rest_framework import serializers

from .models import Track, Course, Student, CourseGroup, Take, Hug


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CourseSerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedRelatedField(source='id', read_only=True, view_name='course-detail')

    class Meta:
        model = Course
        fields = ('url', 'course_id', 'data_year', 'name', 'semester', 'points', 'is_given_this_year',
                  'is_corner_stone', 'comment')


class TakeSerializer(DynamicFieldsModelSerializer):
    course = CourseSerializer(fields=('url', 'course_id', 'name', 'semester', 'points'), read_only=True)
    url = serializers.HyperlinkedRelatedField(source='course', view_name='course-detail', queryset=Course.objects.all())
    type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Take
        fields = ('url', 'course', 'year_in_studies', 'semester', 'type')


class CourseGroupSerializer(DynamicFieldsModelSerializer):
    courses = CourseSerializer(fields=('url', 'course_id', 'name', 'semester', 'points'), many=True, read_only=True)

    class Meta:
        model = CourseGroup
        fields = ('track', 'course_type', 'year_in_studies', 'index_in_track_year', 'courses',
                  'required_course_count', 'required_points', 'comment')


class HugSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Hug
        fields = ('course',)


class TrackSerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedRelatedField(source='id', read_only=True, view_name='track-detail')
    course_groups = CourseGroupSerializer(source='coursegroup_set', many=True, read_only=True)
    total_points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Track
        fields = ('url', 'track_number', 'name', 'data_year', 'total_points', 'points_must', 'points_from_list',
                  'points_choice', 'points_complementary', 'points_corner_stones',
                  'points_minor', 'points_additional_hug', 'comment', 'course_groups')


class StudentSerializer(DynamicFieldsModelSerializer):
    courses = TakeSerializer(source='take_set', many=True)
    url = serializers.HyperlinkedRelatedField(source='id', view_name='student-detail',
                                              read_only=True)

    track_url = serializers.HyperlinkedRelatedField(source='track', view_name='track-detail',
                                                    queryset=Track.objects.all())
    track = TrackSerializer(fields=('track_number', 'name'), read_only=True)
    remaining = serializers.JSONField(read_only=True)

    class Meta:
        model = Student
        fields = ('url', 'track_url', 'track', 'name', 'year_in_studies', 'remaining', 'courses')

    def create(self, validated_data):
        logging.error(validated_data)
        take_set = validated_data.pop('take_set')
        student = Student.objects.create(**validated_data)
        for take in take_set:
            Take.objects.create(student=student, **take)
        return student

    def update(self, student: Student, validated_data):
        logging.error(validated_data)
        take_set = validated_data.pop('take_set')

        student.name = validated_data.get('name', student.name)
        student.track = validated_data.get('track', student.track)
        student.courses.clear()
        for take in take_set:
            Take.objects.create(student=student,
                                course=take['course'],
                                year_in_studies=take['year_in_studies'],
                                semester=take['semester'])

        return student
