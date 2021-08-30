from rest_api.serializers.DynamicSerializer import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_api.models import Course, Track
from rest_api.rest_utils import get_course_type


class CourseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_id', 'data_year', 'name', 'semester', 'points', 'is_given_this_year',
                  'is_corner_stone', 'comment')
        read_only_fields = ('id',)

class CourseOfTrackSerializer(CourseSerializer):
    type = serializers.SerializerMethodField(method_name='get_type')

    def get_type(self, obj):
        request = self.context['request']
        track_id = request.parser_context["kwargs"]["track_pk"]
        track = Track.objects.get(id=track_id)
        return get_course_type(track, obj)


    class Meta:
        model = Course
        fields = CourseSerializer.Meta.fields + ('type', )