from django.shortcuts import render, get_object_or_404
from .models import Book, Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import BookSearchForm


def book_list(request):
    object_list = Book.objects.all()
    paginator = Paginator(object_list, 30)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'books/book/list.html', {'page': page, 'books': books})


def book_detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    return render(request, 'books/book/detail.html', {'book': book})


def book_added(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    request.user.profile.books.add(book)
    request.user.profile.save()
    return render(request, 'books/book/detail.html', {'book': book})


def course_list(request):
    object_list = Course.objects.all()
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'books/course/list.html', {'page': page, 'courses': courses})


def course_detail(request, kurs):
    course = get_object_or_404(Course, kurs=kurs)
    return render(request, 'books/course/detail.html', {'course': course})


def book_search(request):
    form = BookSearchForm()
    query = None
    results = None
    if 'query' in request.GET:
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'description')
            search_query = SearchQuery(query)
            results = Book.objects.all().annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank', '-issued')
    return render(request, 'books/book/search.html', {'form': form, 'query': query, 'results': results})
