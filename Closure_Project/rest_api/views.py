# Create your views here
from django.db.models import Case, When
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
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


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('course_id', 'data_year', 'points')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^course_id')


class MyTrackCourses(viewsets.ModelViewSet):
    def _get_queryset(self, only_must: bool):
        user = self.request.user
        student = Student.objects.get(user=user)
        track = student.track
        if not track:
            return Course.objects.none()

        # get the courses list and preserve the order
        pk_list = student.track.course_pks(only_must=only_must)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])

        return Course.objects.filter(pk__in=pk_list).order_by(preserved)

    def get_queryset(self):
        return self._get_queryset(False)

    @action(detail=False)
    def get_must(self):
        return self._get_queryset(True)

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
        return Student.objects.filter(user=self.request.user)

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
    filter_fields = ('user__username', 'year_in_studies', 'track__track_number',
                     'courses__course_id')
    pagination_class = ResultSetPagination
    search_fields = ('user__username', 'year_in_studies', '^track__track_number',
                     '^courses__course_id')


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('track_number')
    serializer_class = TrackSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'track_number')
    pagination_class = ResultSetPagination
    search_fields = ('name', '^track_number')


class TakeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Take.objects.all().order_by('course')
    serializer_class = TakeSerializer
