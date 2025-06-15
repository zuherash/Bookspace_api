from django.db import models
from django.contrib.auth.models import User


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hired_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    librarian = models.ForeignKey(
        Librarian,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
    )
    readers = models.ManyToManyField(Reader, related_name="books", blank=True)
    available = models.BooleanField(default=True)
    is_borrowable = models.BooleanField(default=True)
    is_buyable = models.BooleanField(default=True)
    copies_available = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk}"


class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.pk}"
