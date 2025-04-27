from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination

class Bookpagination(PageNumberPagination):
    page_size='5'

class BookRetrieveAPIView(generics.RetrieveAPIView):
    queryset=Book.objects.all()
    serializer_class= BookSerializer
    lookup_field='id'

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = Bookpagination
