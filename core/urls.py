from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    UserRegistrationAPIView,
    OrderListCreateAPIView,
    )


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('auth/register/', UserRegistrationAPIView.as_view(), name='register'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),

]
