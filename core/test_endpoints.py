from django.contrib.auth.models import User
from django.test import override_settings, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import Book


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class EndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('register')
        response = self.client.post(url, {"username": "alice", "password": "pass"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_user_login(self):
        User.objects.create_user(username="bob", password="secret")
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"username": "bob", "password": "secret"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_book_crud_flow(self):
        # Create
        create_resp = self.client.post(reverse('book-list-create'), {
            "title": "Django 101",
            "author": "Someone",
            "description": "Intro",
            "available": True,
        })
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        book_id = create_resp.data["id"]

        # Retrieve
        retrieve_resp = self.client.get(reverse('book-detail', args=[book_id]))
        self.assertEqual(retrieve_resp.status_code, status.HTTP_200_OK)

        # Update
        update_resp = self.client.put(reverse('book-detail', args=[book_id]), {
            "title": "Django 102",
            "author": "Someone",
            "description": "Intro",
            "available": True,
        })
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(update_resp.data["title"], "Django 102")

        # Delete
        delete_resp = self.client.delete(reverse('book-detail', args=[book_id]))
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_creation(self):
        user = User.objects.create_user(username="carol", password="pass")
        book = Book.objects.create(title="API", author="Dev", description="Desc")
        token = self.client.post(reverse('token_obtain_pair'), {
            "username": "carol",
            "password": "pass",
        }).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(reverse('order-list-create'), {
            "user": user.id,
            "book": book.id,
            "quantity": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_borrow_and_buy(self):
        book = Book.objects.create(title="Borrow", author="Auth", copies_available=2)
        borrow_url = reverse('book-borrow', args=[book.id])
        resp1 = self.client.post(borrow_url)
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assertEqual(resp1.data["copies_available"], 1)
        book.refresh_from_db()
        self.assertEqual(book.copies_available, 1)

        resp2 = self.client.post(borrow_url)
        book.refresh_from_db()
        self.assertEqual(resp2.data["copies_available"], 0)
        self.assertFalse(book.available)

        buy_book = Book.objects.create(title="Buy", author="Auth", copies_available=1)
        buy_url = reverse('book-buy', args=[buy_book.id])
        buy_resp = self.client.post(buy_url)
        self.assertEqual(buy_resp.status_code, status.HTTP_200_OK)
        buy_book.refresh_from_db()
        self.assertEqual(buy_book.copies_available, 0)
        self.assertFalse(buy_book.available)

