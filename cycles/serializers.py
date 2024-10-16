from rest_framework import serializers
from .models import SuperCycle, Cycle

class SuperCyCleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperCycle
        fields = ['id', 'created_at']
        read_only_fields = ['id', 'created_at']


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ['id', 'requests']
