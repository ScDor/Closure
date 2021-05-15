from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Student, CourseGroup, Track, Take
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(CourseGroup)
admin.site.register(Track)
admin.site.register(Take)


