from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from .filters import BookFilter
from .models import Book
from .views import BookPagination


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class BookFilterTests(TestCase):
    def test_filter_meta_model(self):
        self.assertEqual(BookFilter.Meta.model, Book)

    def test_filter_fields(self):
        self.assertListEqual(
            BookFilter.Meta.fields,
            ["title", "author", "available"],
        )


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class PaginationTests(TestCase):
    def test_page_size_integer(self):
        self.assertEqual(BookPagination.page_size, 5)

    def test_pagination_returns_five_results(self):
        for i in range(7):
            Book.objects.create(title=f"Book {i}", author="Author")

        factory = APIRequestFactory()
        wsgi_request = factory.get("/books/")
        request = Request(wsgi_request)
        paginator = BookPagination()

        page = paginator.paginate_queryset(Book.objects.all(), request)
        self.assertEqual(len(page), 5)

