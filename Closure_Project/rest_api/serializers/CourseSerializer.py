from rest_api.serializers.DynamicSerializer import *
from rest_api.models import Course


class CourseSerializer(DynamicFieldsModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(source='id', read_only=True)

    class Meta:
        model = Course
        fields = ('pk', 'course_id', 'data_year', 'name', 'semester', 'points', 'is_given_this_year',
                  'is_corner_stone', 'comment')
