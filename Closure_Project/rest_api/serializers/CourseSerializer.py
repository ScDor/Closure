from typing import Optional
from rest_api.serializers.DynamicSerializer import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_api.models import Course, CourseType, Track
from rest_api.rest_utils import get_course_type

class CourseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_id', 'data_year', 'name', 'semester', 'points', 'is_given_this_year',
                  'is_corner_stone', 'comment')
        read_only_fields = ('id',)

class CourseOfTrackSerializer(CourseSerializer):
    type = serializers.SerializerMethodField(method_name='get_type')

    def get_type(self, obj) -> Optional[CourseType]:

        # try obtaining track ID set by a parent serializer (e.g, 
        # DetailCoursePlanSerializer)
        track_id = self.context.get("track_pk", None)

        if not track_id:
            # otherwise, try obtaining it from the HTTP request,
            # if its of the form /tracks/:track_pk/...
            request = self.context['request']
            track_id = request.parser_context["kwargs"].get("track_pk", None)

        if track_id:
            track = Track.objects.get(id=track_id)
            return get_course_type(track, obj)

        return None

    class Meta:
        model = Course
        fields = CourseSerializer.Meta.fields + ('type', )