from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'course_groups', views.CourseGroupViewSet)
router.register(r'students', views.StudentGroupViewSet)
router.register(r'tracks', views.TrackGroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/v1/', include(router.urls)),
]