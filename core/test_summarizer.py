from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class SummarizerEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_summarize_endpoint(self):
        url = reverse('summarize')
        text = "This is a sentence. " * 5
        response = self.client.post(url, {"text": text})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("summary", response.data)

    def test_missing_text_returns_error(self):
        url = reverse('summarize')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
