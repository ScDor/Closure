# Create your views here
from rest_framework import viewsets
from .pagination import ResultSetPagination

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters



from .models import Course, Student, CourseGroup, Track, Take
from .serializers import CourseSerializer, CourseGroupSerializer, StudentSerializer, TrackGroupSerializer, \
    TakeSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer
    lookup_field = 'course_id'
    filter_backends = [filters.SearchFilter]
    pagination_class = ResultSetPagination
    search_fields = ('name', 'course_id')


class CourseGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = CourseGroup.objects.all().order_by('track')
    serializer_class = CourseGroupSerializer

    # def get_object(self):
    #     course_id = self.kwargs['id']
    #     return self.queryset.filter(course_id=course_id)


class StudentGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer


class TrackGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('track_number')
    serializer_class = TrackGroupSerializer


class TakeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Take.objects.all().order_by('course')
    serializer_class = TakeSerializer

