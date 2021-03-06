from django.contrib.auth.models import User

from rest_api.serializers.DynamicSerializer import *
from rest_api.models import Student, Take, Track
from .TakeSerializer import TakeSerializer
from .TrackSerializer import TrackSerializer

from django.shortcuts import get_object_or_404


class StudentSerializer(DynamicFieldsModelSerializer):
    courses = TakeSerializer(source='take_set', many=True)
    pk = serializers.PrimaryKeyRelatedField(source='id',
                                            read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    track_pk = serializers.PrimaryKeyRelatedField(source='track',
                                                  queryset=Track.objects.all())
    track = TrackSerializer(fields=('track_number', 'name'), read_only=True)
    remaining = serializers.JSONField(read_only=True)

    class Meta:
        model = Student
        fields = ('pk', 'username', 'track_pk', 'track', 'year_in_studies', 'remaining', 'courses')

    def update(self, student: Student, validated_data):
        take_set = validated_data.pop('take_set')
        student.track = validated_data.get('track', student.track)
        student.year_in_studies = validated_data.get('year_in_studies', student.year_in_studies)
        student.courses.clear()
        for take in take_set:
            Take.objects.create(student=student,
                                course=take['course'],
                                year_in_studies=take['year_in_studies'],
                                semester=take['semester'])

        student.save()
        return student
