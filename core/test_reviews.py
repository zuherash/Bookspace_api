from django.contrib.auth.models import User
from django.test import override_settings, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import Book, Review


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class ReviewEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="reviewer", password="pass")
        self.book = Book.objects.create(title="Test Book", author="Author")

    def test_review_crud_flow(self):
        # Create
        create_resp = self.client.post(reverse('review-list-create'), {
            "user": self.user.id,
            "book": self.book.id,
            "rating": 5,
            "comment": "Great!"
        })
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        review_id = create_resp.data["id"]

        # Retrieve
        retrieve_resp = self.client.get(reverse('review-detail', args=[review_id]))
        self.assertEqual(retrieve_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_resp.data["rating"], 5)

        # Update
        update_resp = self.client.put(reverse('review-detail', args=[review_id]), {
            "user": self.user.id,
            "book": self.book.id,
            "rating": 4,
            "comment": "Good"
        })
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(update_resp.data["rating"], 4)

        # Delete
        delete_resp = self.client.delete(reverse('review-detail', args=[review_id]))
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)
