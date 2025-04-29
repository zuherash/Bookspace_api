from .models import Book
from rest_framework import serializers
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'
    
class Registerserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)
    
    class meta:
        model = User
        fields= ['username','email','password']
    
    def create(self,validated_data):
        user = user.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']            
        )
        return user
    