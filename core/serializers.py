from .models import Book,Invoice,Reviews,Comment
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'available', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class Registerserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(queryset=Reviews.objects.all())
    
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'text', 'created_at']


class Reviewserializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Reviews
        fields = ['id', 'book', 'user', 'rating', 'text', 'created_at', 'comments']