from rest_framework import serializers
from .models import Request, Comments
from files.serializers import FileSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['content']

class RequestSerializerMin(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'uploaded_at', 'status', 'type', 'uploaded_at', 'user']

class RequestSerializerMax(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True)
    file = FileSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['comment', 'user', 'id', 'uploaded_at', 'status', 'type']
