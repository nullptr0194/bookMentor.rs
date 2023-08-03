from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, GradedCourse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, AddCourseForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from books.models import get_courses_by_module, Course
from account.algorithms import *
import os
from books.models import Book


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            prof = Profile.objects.create(user=new_user)
            prof.books.clear()
            prof.save()

            # FORSIRATI KORISNIKA DA SE NAKON REGISTRACIJE PREBACI NA EDITOVANJE PROFILA

            return render(request, 'account/register_done.html', {'new_user': new_user})
            # request.user = new_user
            # return edit(request)
        else:
            user_form = UserRegistrationForm()
            return render(request, 'account/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error while updating.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required
def book_list(request):
    object_list = request.user.profile.books.all()
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'account/books/list.html', {'page': page, 'books': books})


@login_required
def course_list(request):  # smer i godina su bitni da se uzmu, na osnovu njih dobiti sve kurseve
    module = request.user.profile.smer
    year = request.user.profile.godina
    object_list = get_courses_by_module(module, year, request.user.profile)
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'account/courses/list.html', {'page': page, 'courses': courses})


@login_required
def course_detail(request, kurs):
    course_form = None
    grade = None
    course = get_object_or_404(Course, kurs=kurs)
    if 'grade' in request.GET:
        course_form = AddCourseForm(request.GET)
        if course_form.is_valid():
            grade = int(course_form.cleaned_data['grade'])
            graded_course = GradedCourse(profile=request.user.profile, course=course, grade=grade)
            graded_course.save()
            path = os.path.join('static', 'profile_coefficients.csv')
            update_csv(path, request.user.profile.pk,
                       graded_course.course.get_topics_dict(), grade)
            messages.success(request, 'Added successfully!')
            return render(request, 'account/dashboard.html')
        else:
            messages.error(request, 'Error while updating.')
            return render(request, 'account/courses/detail.html', {'form': course_form, 'course': course})

    else:
        course_form = AddCourseForm()
    return render(request, 'account/courses/detail.html', {'form': course_form, 'course': course})


@login_required
def course_mine(request):
    object_list = GradedCourse.objects.all().filter(profile=request.user.profile)
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'account/courses/list_mine.html', {'page': page, 'graded_courses': courses})


@login_required
def recommend(request):
    profile = request.user.profile.pk
    path = os.path.join('static', 'profile_coefficients.csv')
    data = pd.read_csv(path, low_memory=False)
    data.set_index('profile', inplace=True)
    data = data.iloc[:, 1:]
    # print(data)
    recommended_books_dict = build(data, profile)
    description_rec(data, profile, recommended_books_dict)
    # recommended_books_dict = sorted(recommended_books_dict.values(), key=lambda x: x)
    object_recommended_books = get_books_from_dict(recommended_books_dict)
    paginator = Paginator(object_recommended_books, 5)
    page = request.GET.get('page')
    try:
        recommended_books = paginator.page(page)
    except PageNotAnInteger:
        recommended_books = paginator.page(1)
    except EmptyPage:
        recommended_books = paginator.page(paginator.num_pages)
    return render(request, 'account/recommend/recommend.html', {'page': page, 'recommended_books': recommended_books})
