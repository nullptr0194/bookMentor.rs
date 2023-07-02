from django.contrib import admin
from .models import Profile, GradedCourse


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'smer', 'godina']
    list_filter = ('smer', 'godina')
    raw_id_fields = ['books']


@admin.register(GradedCourse)
class GradedCourseAdmin(admin.ModelAdmin):
    list_display = ['profile', 'course', 'grade']
