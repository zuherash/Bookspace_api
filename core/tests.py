from django.test import TestCase, override_settings

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

