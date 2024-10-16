from rest_framework import serializers
from .models import ActivityPlanner
from files.serializers import FileSerializer


class RequestSerializerMin(serializers.ModelSerializer):
    class Meta:
        model = ActivityPlanner
        fields = ['id', 'uploaded_at', 'status', 'type', 'user']

class RequestSerializerMax(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)
    class Meta:
        model = ActivityPlanner
        fields = ['comment', 'user', 'id', 'uploaded_at', 'status', 'type', 'file', 'reviewed_by']
