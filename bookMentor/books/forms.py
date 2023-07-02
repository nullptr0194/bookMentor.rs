from .models import Book, Course
from django import forms


class BookSearchForm(forms.Form):
    query = forms.CharField()
