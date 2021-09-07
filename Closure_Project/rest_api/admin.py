from django.contrib import admin

# Register your models here.
from .models import Course, Student, CourseGroup, Track, Take, CoursePlan
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(CourseGroup)
admin.site.register(Track)
admin.site.register(Take)
admin.site.register(CoursePlan)