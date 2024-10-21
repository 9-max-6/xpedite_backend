from rest_framework import serializers
from .models import Request
from files.serializers import FileSerializerMin
from users.serializers import UserSerializer


class RequestSerializerMin(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Request
        fields = ['id', 'uploaded_at', 'status', 'type', 'user', 'total']

class RequestSerializerMax(serializers.ModelSerializer):
    user = UserSerializer()
    file = FileSerializerMin()
    reviewed_by_finance = serializers.SerializerMethodField()
    reviewed_by_sup = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ['comment', 'user', 'finance_comment', 'id', 'uploaded_at', 'status', 'type', 'file', 'reviewed_by_finance', 'reviewed_by_sup', 'description', 'title']

    def get_reviewed_by_finance(self, obj):
        # Return the first user, or any other logic to select a single user
        user = obj.reviewed_by_finance.first()
        if user:
            return UserSerializer(user).data
        return None

    def get_reviewed_by_sup(self, obj):
        # Return the first user, or any other logic to select a single user
        user = obj.reviewed_by_sup.first()
        if user:
            return UserSerializer(user).data
        return None

class RequestSerializerMake(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'uploaded_at', 'status', 'type', 'file', 'total', 'description', 'title' ]


