from rest_framework import serializers
from .models import SuperCycle, Cycle
from requests.serializers import RequestSerializerMin

class SuperCyCleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperCycle
        fields = ['id', 'created_at', 'title']
        read_only_fields = ['id', 'created_at']


class CycleSerializer(serializers.ModelSerializer):
    requests = RequestSerializerMin()
    class Meta:
        model = Cycle
        fields = ['id', 'requests']
