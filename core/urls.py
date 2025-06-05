from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    UserRegistrationAPIView,
    OrderListCreateAPIView,
    ReviewListCreateAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
    )


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('auth/register/', UserRegistrationAPIView.as_view(), name='register'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),

]
