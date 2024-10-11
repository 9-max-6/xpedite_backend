from rest_framework import serializers
from .models import CustomUser  # Assuming you have a User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']  # Adjust the fields according to your User model
