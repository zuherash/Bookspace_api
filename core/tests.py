from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book,Reviews,Comment

class BookTests(APITestCase):
    def setUp(self):
        # إنشاء مستخدم للاختبارات
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # توليد توكن JWT لهذا المستخدم
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_create_book(self):
        # تمرير التوكن ضمن Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # البيانات التي سنرسلها لإنشاء كتاب
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'description': 'A test book.',
            'available': True
        }
        # إرسال طلب POST لإنشاء كتاب
        response = self.client.post('/api/books/', data, format='json')
        print(response.data)

        # التحقق أن الرد يعيد 201 Created
        self.assertEqual(response.status_code, 201)
        
        # التحقق أن الكتاب تمت إضافته فعلًا بقاعدة البيانات
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

class ReviewTests(APITestCase):
    def setUp(self):
        # نعمل مستخدم وكتاب لنربط فيهم المراجعة
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Author Name',
            description='A test book.',
            available=True,
            user=self.user
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'book': self.book.id,
            'rating': 5,
            'text': 'Amazing book!'
        }
        response = self.client.post('/api/reviews/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertEqual(Reviews.objects.get().text, 'Amazing book!')

    def test_get_review_list(self):
        # أنشئ مراجعة يدويًا
        Reviews.objects.create(book=self.book, user=self.user, rating=4, text='Great read!')
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Author Name',
            description='A test book.',
            available=True,
            user=self.user
        )
        self.review = Reviews.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            text='Excellent book!'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'review': self.review.id,
            'text': 'I agree with this review!'
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, 'I agree with this review!')

    def test_get_comment_list(self):
        Comment.objects.create(review=self.review, user=self.user, text='Interesting point.')
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)