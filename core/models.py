from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    def __str__(self):
        return self.title
class Invoice(models.Model):
    INVOICE_TYPES = [
        ('Purchase','purchase'),
        ('Sell','sell'),
    ]
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Invoice_type = models.CharField(max_length=10,choices=INVOICE_TYPES)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.invoice_type} - {self.book.title} - {self.amount}"
    