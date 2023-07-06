from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('books/', views.book_list, name='book_list'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:kurs>/', views.course_detail, name='course_detail'),
    path('courses/my-courses/list/', views.course_mine, name='course_mine'),
    path('recommend/', views.recommend, name='recommend'),
]
