from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:isbn>/', views.book_detail, name='book_detail'),
    path('<int:isbn>/added/', views.book_added, name='book_added'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:kurs>/', views.course_detail, name='course_detail'),
    path('search/', views.book_search, name='book_search'),
]
