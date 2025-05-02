from rest_framework import generics
from .models import Book,Invoice,Reviews,Comment
from .serializers import BookSerializer,InvoiceSerializer,CommentSerializer,Reviewserializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import BookFilter
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import Registerserializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .permissions import IsAdminOrAccountant,IsAuditorReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
class InvoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated,IsAdminOrAccountant]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
class InvoiceDetailAPIView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated,IsAdminOrAccountant|IsAuditorReadOnly]
class ReviewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = Reviewserializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = Reviewserializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = Registerserializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()   # احفظ المستخدم الجديد
            refresh = RefreshToken.for_user(user)  # توليد التوكن لهالمستخدم
            return Response({
                'message': 'User Registered Successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



