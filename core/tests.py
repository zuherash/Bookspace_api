from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book,Reviews,Comment
from rest_framework import status
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
class BookPermissionTests(APITestCase):
    def setUp(self):
        # صاحب الكتاب
        self.owner = User.objects.create_user(username='owner', password='ownerpass')
        self.owner_token = str(RefreshToken.for_user(self.owner).access_token)

        # مستخدم آخر
        self.other_user = User.objects.create_user(username='other', password='otherpass')
        self.other_token = str(RefreshToken.for_user(self.other_user).access_token)

        # إنشاء كتاب باسم المالك
        self.book = Book.objects.create(title='Test Book', author='Author', description='Desc', available=True, user=self.owner)
        
        self.user = self.owner
        self.token = self.owner_token

    def test_owner_can_update_book(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        
    def test_other_user_cannot_update_book(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.other_token)
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_update_book_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        book = Book.objects.create(title='Old Title', author='Old Author', description='Old', available=True, user=self.user)
        data = {'title': 'New Title', 'author': 'New Author', 'description': 'Updated', 'available': False}
        response = self.client.put(f'/api/books/{book.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        updated_book = Book.objects.get(id=book.id)
        self.assertEqual(updated_book.title, 'New Title')
        
        
        
    def test_update_book_by_non_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_token = str(RefreshToken.for_user(other_user).access_token)
        book = Book.objects.create(title='Owner Book', author='Owner Author', description='Desc', available=True, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + other_token)
        data = {'title': 'Hacked Title'}
        response = self.client.put(f'/api/books/{book.id}/', data, format='json')
        self.assertEqual(response.status_code, 403)  # ممنوع
    def test_delete_book_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        book = Book.objects.create(title='Delete Me', author='Author', description='Desc', available=True, user=self.user)
    
        response = self.client.delete(f'/api/books/{book.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(id=book.id).exists())
        
    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        book = Book.objects.create(title='Review Book', author='Author', description='Desc', available=True, user=self.user)
    
        data = {'book': book.id, 'rating': 5, 'text': 'Great book!'}
        response = self.client.post('/api/reviews/', data, format='json')
    
        self.assertEqual(response.status_code, 201)

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        book = Book.objects.create(title='Comment Book', author='Author', description='Desc', available=True, user=self.user)
        review = Reviews.objects.create(book=book, user=self.user, rating=5, text='Nice!')
    
        data = {'review': review.id, 'text': 'Totally agree!'}
        response = self.client.post('/api/comments/', data, format='json')
    
        self.assertEqual(response.status_code, 201)
