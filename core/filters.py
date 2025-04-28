import django_filters
from .models import Book

class BookFilter(django_filters.filterset):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    available = django_filters.BooleanFilter()
    
    class meta:
        model = Book
        fields = ['title','author','avialable']