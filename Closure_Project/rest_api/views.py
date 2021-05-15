# Create your views here

from rest_framework import viewsets

from .models import Course, Student, CourseGroup, Track
from .serializers import CourseSerializer, CourseGroupSerializer, StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer


class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer


class TrackGroupViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer
