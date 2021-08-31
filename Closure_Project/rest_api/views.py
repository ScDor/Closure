# Create your views here
from django.db.models import Case, When, Q
from django.utils.timezone import make_aware
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from datetime import datetime

from rest_framework_nested.viewsets import NestedViewSetMixin
from .permissions import CoursePlanPermission, IsAdminOrAuthenticatedReadOnly
from .models import Course, CourseType, Student, CourseGroup, Track, Take, CoursePlan
from .pagination import ResultSetPagination

from .serializers.CourseSerializer import CourseSerializer, CourseOfTrackSerializer
from .serializers.CourseGroupSerializer import CourseGroupSerializer
from .serializers.StudentSerializer import StudentSerializer
from .serializers.TrackSerializer import TrackSerializer, TrackSerializerWithCourseGroups
from .serializers.CoursePlanSerializer import TakeSerializer, DetailTakeSerializer, CoursePlanSerializer, DetailCoursePlanSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('course_id', 'data_year', 'points')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^course_id')

class TrackCoursesViewSet(CourseViewSet, NestedViewSetMixin):
    filter_fields = CourseViewSet.filter_fields + ('coursegroup__course_type', )
    serializer_class = CourseOfTrackSerializer
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            relevant_cgs = CourseGroup.objects.all()
        else:
            relevant_cgs = CourseGroup.objects.filter(track=self.kwargs['track_pk'])
        courses = Course.objects.filter(coursegroup__in=relevant_cgs)
        return courses

class MyTrackCourses(viewsets.ModelViewSet):
    def _get_queryset(self, only_must: bool):
        user = self.request.user.id
        student = Student.objects.filter(user=user).first()
        if student is None:
            return Course.objects.none()
        track = student.track
        if not track:
            return Course.objects.none()

        # get the courses list and preserve the order
        pk_list = student.track.course_pks(only_must=only_must)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])

        return Course.objects.filter(pk__in=pk_list).order_by(preserved)

    def get_queryset(self):
        if self.action == 'must':
            return self._get_queryset(True)
        return self._get_queryset(False)

    @action(methods=['GET'], detail=False)
    def must(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    serializer_class = CourseSerializer
    filter_fields = ('course_id', 'data_year', 'points')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^course_id')


class StudentMeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post']

    def get_object(self):
        queryset = self.get_queryset()
        if not queryset:
            return
        return queryset[0]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        if not self.get_object():
            return Response({'error': 'Bad token'}, status=401)
        return self.retrieve(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)


class CourseGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    pagination_class = ResultSetPagination
    queryset = CourseGroup.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer


class StudentGroupViewSet(viewsets.ModelViewSet):
    # this view set is for administration
    permission_classes = (IsAdminUser,)
    queryset = Student.objects.all().order_by('user__username')
    serializer_class = StudentSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('user__username',)
    pagination_class = ResultSetPagination
    search_fields = ('user__username',)


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    queryset = Track.objects.all().order_by('track_number')
    serializer_class = TrackSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'data_year', 'track_number')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^track_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return TrackSerializer
        return TrackSerializerWithCourseGroups

class TakeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Take.objects.all().order_by('course')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailTakeSerializer
        return TakeSerializer

class CoursePlanViewSet(viewsets.ModelViewSet):
    permission_classes = (CoursePlanPermission,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailCoursePlanSerializer
        return CoursePlanSerializer

    def get_queryset(self):

        public_plans = Q(public=True)

        if not self.request.user or not self.request.user.is_authenticated:
            return CoursePlan.objects.filter(public_plans)
        student = Student.objects.get(user=self.request.user.id)
        student = get_request_student(self.request)
        return CoursePlan.objects.filter(Q(owner=student) | public_plans)
    
    def perform_create(self, serializer):
        student = get_request_student(self.request)
        serializer.save(owner=student)

    def perform_update(self, serializer):
        serializer.save(modified_at=make_aware(datetime.now()))


def get_request_student(req: HttpRequest) -> Student:
    return Student.objects.get(user=req.user.id)