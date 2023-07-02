from django.contrib import admin
from .models import Book, Course


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title', 'issued', 'authors', 'publishers', 'cover_url', 'topic')
    list_filter = ('issued',)
    search_fields = ('isbn', 'title', 'description')
    date_hierarchy = 'issued'
    ordering = ('-issued',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'kurs', 'o_i', 'simingod', 'irmingod', 'osmingod', 'otmingod', 'ogmingod', 'ofmingod', 'oemingod', 'topics')
    list_filter = ('o_i',)
    search_fields = ('kurs', 'o_i', 'topics')
    ordering = ('id',)
