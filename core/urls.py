from django.urls import path
from .views import BookListCreateAPIView,BookRetrieveAPIView,BookUpdateAPIView

urlpatterns = [    
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("books/<int:pk>", BookRetrieveAPIView.as_view(), name="book-detail"),
    path("books/<int:pk>/update", BookUpdateAPIView.as_view(), name="book-update"),
]
