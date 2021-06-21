# Create your views here
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Course, Student, CourseGroup, Track, Take
from .pagination import ResultSetPagination

from .serializers.CourseSerializer import CourseSerializer
from .serializers.CourseGroupSerializer import CourseGroupSerializer
from .serializers.StudentSerializer import StudentSerializer
from .serializers.TrackSerializer import TrackSerializer
from .serializers.TakeSerializer import TakeSerializer

from rest_api.utils import get_course_type
from django.shortcuts import get_object_or_404


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('course_id', 'data_year',)
    pagination_class = ResultSetPagination
    search_fields = ('name', '^course_id')

    @action(detail=True, methods=['GET'], url_path='get_course_type/(?P<track_pk>[^/.]+)')
    def get_course_type(self, request, track_pk, pk=None):
        course = self.get_object()
        track = get_object_or_404(Track, pk=track_pk)
        return Response({'type': get_course_type(track, course)})


class CourseGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = ResultSetPagination
    queryset = CourseGroup.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer


class StudentGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all().order_by('user__first_name')
    serializer_class = StudentSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = ResultSetPagination
    search_fields = ('user__username', 'courses__name', '^courses__course_id')


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('track_number')
    serializer_class = TrackSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'track_number')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^track_number')

    @action(detail=True, methods=['GET'], url_path='get_course_type/(?P<course_pk>[^/.]+)')
    def get_course_type(self, request, course_pk, pk=None):
        track = self.get_object()
        course = get_object_or_404(Course, pk=course_pk)
        return Response({'type': get_course_type(track, course)})


class TakeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Take.objects.all().order_by('course')
    serializer_class = TakeSerializer

class StudentTakeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Take.objects.all().order_by('course')
    serializer_class = TakeSerializer

    def get_queryset(self):
        return self.request.user.courses.all()