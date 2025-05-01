from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
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
        serializer.save(User=self.request.user)
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = Registerserializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            refresh = RefreshToken.for_user(User)
            return Response({'message':'User Registered Succesfuly',
                    'referesh':str(refresh),
                    'access' :str(refresh.access_token)
                            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



