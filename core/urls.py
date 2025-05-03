from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    InvoiceListCreateAPIView,
    InvoiceDetailAPIView,
    ReviewsListCreateAPIView,
    ReviewsDetailAPIView,
    CommentDetailAPIView,
    CommentListCreateAPIView
    )
from .views import register


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path("register/", register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("invoices/", InvoiceListCreateAPIView.as_view(), name="invoice_list_create"),
    path("invoices/<int:pk>/", InvoiceDetailAPIView.as_view(), name="invoice_detail"),
    path('reviews/', ReviewsListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewsDetailAPIView.as_view(), name='review-detail'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
