import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(lookup_expr="icontains")
    available = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'available']
