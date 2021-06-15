from rest_api.serializers.DynamicSerializer import *
from rest_api.models import Course, Take
from .CourseSerializer import CourseSerializer


class TakeSerializer(DynamicFieldsModelSerializer):
    course = CourseSerializer(fields=('id', 'course_id', 'name', 'semester', 'points'), read_only=True)
    pk = serializers.PrimaryKeyRelatedField(source='course', queryset=Course.objects.all())
    type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Take
        fields = ('pk', 'course', 'year_in_studies', 'semester', 'type')
