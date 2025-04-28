from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import BookFilter

class Bookpagination(PageNumberPagination):
    page_size='5'
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = Bookpagination
    filter_backends = [DjangoFilterBackend , filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title','author']
    ordering_fields = ['title','created_at']
    ordering = ['-created_at']
    
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'




