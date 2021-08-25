from rest_api.serializers.DynamicSerializer import *
from rest_api.models import CourseGroup
from .CourseSerializer import CourseSerializer


class CourseGroupSerializer(DynamicFieldsModelSerializer):
    courses = CourseSerializer(fields=('pk', 'course_id', 'name', 'semester', 'points'), many=True, read_only=True)

    class Meta:
        model = CourseGroup
        fields = ('track', 'data_year', 'course_type', 'year_in_studies', 'index_in_track_year', 'courses',
                  'required_course_count', 'required_points', 'comment')
