from django.contrib import admin

from .models import Book, Order, Review, Librarian, Reader

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Librarian)
admin.site.register(Reader)
