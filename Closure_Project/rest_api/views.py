# Create your views here
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import serializers
from .models import Course, Student, CourseGroup, Track, Take
from .pagination import ResultSetPagination
from .serializers import CourseSerializer, CourseGroupSerializer, StudentSerializer, TrackSerializer, \
    TakeSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('course_id', 'data_year',)
    pagination_class = ResultSetPagination
    search_fields = ('name', '^course_id')


class CourseGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = ResultSetPagination
    queryset = CourseGroup.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer


class StudentGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer
    filter_backends = (filters.SearchFilter, )
    pagination_class = ResultSetPagination
    search_fields = ('name', 'courses__name', '^courses__course_id')


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('track_number')
    serializer_class = TrackSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'track_number')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^track_number')


class TakeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Take.objects.all().order_by('course')
    serializer_class = TakeSerializer
