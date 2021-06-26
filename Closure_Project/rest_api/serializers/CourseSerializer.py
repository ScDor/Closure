from rest_api.serializers.DynamicSerializer import *
from rest_api.models import Course, Student, CourseType
from rest_api.rest_utils import get_course_type


class CourseSerializer(DynamicFieldsModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(source='id', read_only=True)
    type = serializers.SerializerMethodField(method_name='get_type')

    def get_type(self, obj):
        user = self.context.get('request').user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return None
        return get_course_type(student.track, obj)

    class Meta:
        model = Course
        fields = ('pk', 'course_id', 'data_year', 'name', 'semester', 'points', 'type', 'is_given_this_year',
                  'is_corner_stone', 'comment')
