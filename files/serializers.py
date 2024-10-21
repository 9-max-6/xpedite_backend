from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_name', 'uploaded_at', 'user', 'file_content']
        read_only_fields = ['id', 'created_at']

class FileSerializerMin(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_name',]
