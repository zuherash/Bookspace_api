from models import Book
from rest_framework import serializers


class Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'
    
