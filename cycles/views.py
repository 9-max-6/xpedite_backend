from rest_framework import viewsets
from requests.permissions import IsManagement
from rest_framework.permissions import IsAuthenticated
from .models import SuperCycle, Cycle
from requests.models import Request
from rest_framework.response import Response
from .serializers import SuperCyCleSerializer, CycleSerializer
from rest_framework.decorators import action

class SuperCycleViewSet(viewsets.ModelViewSet):
    """Cycles"""
    queryset = SuperCycle.objects.order_by('-created_at').all()
    permission_classes = [IsAuthenticated, IsManagement]
    serializer_class = SuperCyCleSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated()]
        return super().get_permissions()

class CycleViewSet(viewsets.ModelViewSet):
    """Cycles"""

    permission_classes = [IsManagement, IsAuthenticated]
    serializer_class = CycleSerializer
    queryset = Cycle.objects.all()
