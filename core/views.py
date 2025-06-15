from django.contrib.auth.models import User
from rest_framework import generics, status
from .models import Book, Order, Review
from .serializers import BookSerializer, UserRegistrationSerializer, OrderSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import BookFilter
from .summarizer import summarize_text

class BookPagination(PageNumberPagination):
    page_size = 5

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend , filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title','author']
    ordering_fields = ['title','created_at']
    ordering = ['-created_at']
    
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


class BookBorrowAPIView(APIView):
    def post(self, request, pk):
        book = generics.get_object_or_404(Book, pk=pk)
        if not book.available or not book.is_borrowable or book.copies_available <= 0:
            return Response({"detail": "Book not available for borrowing."}, status=status.HTTP_400_BAD_REQUEST)
        book.copies_available -= 1
        if book.copies_available == 0:
            book.available = False
        book.save()
        return Response(BookSerializer(book).data)


class BookBuyAPIView(APIView):
    def post(self, request, pk):
        book = generics.get_object_or_404(Book, pk=pk)
        if not book.available or not book.is_buyable or book.copies_available <= 0:
            return Response({"detail": "Book not available for purchase."}, status=status.HTTP_400_BAD_REQUEST)
        book.copies_available -= 1
        if book.copies_available == 0:
            book.available = False
        book.save()
        return Response(BookSerializer(book).data)


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'pk'


class SummarizeAPIView(APIView):
    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response({"detail": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
        summary = summarize_text(text)
        return Response({"summary": summary})




