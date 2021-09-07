from rest_api.serializers.DynamicSerializer import DynamicFieldsModelSerializer, serializers
from rest_api.models import Track
from .CourseGroupSerializer import CourseGroupSerializer


class TrackSerializer(DynamicFieldsModelSerializer):
    total_points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Track
        fields = ('id', 'track_number', 'name', 'data_year', 'total_points', 'points_must', 'points_from_list',
                  'points_choice', 'points_complementary', 'points_corner_stones',
                  'points_minor', 'points_additional_hug', 'comment')
        read_only_fields = ('id',)

class TrackSerializerWithCourseGroups(TrackSerializer):
    course_groups = CourseGroupSerializer(source='coursegroup_set', many=True, read_only=True)

    class Meta:
        model = Track
        fields = TrackSerializer.Meta.fields + ('course_groups', )
