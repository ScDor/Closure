from django.contrib.auth.models import User

from rest_api.serializers.DynamicSerializer import serializers, DynamicFieldsModelSerializer
from rest_api.models import Student, Take, Track
from .CoursePlanSerializer import CoursePlanSerializer
from .TrackSerializer import TrackSerializer

from django.shortcuts import get_object_or_404


class StudentSerializer(DynamicFieldsModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    course_plans = CoursePlanSerializer(source='courseplan_set', many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'username', 'course_plans')
