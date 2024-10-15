from rest_framework import viewsets
from requests.permissions import IsManagement
from .models import SuperCycle, Cycle
from requests.models import Request
from .serializers import SuperCyCleSerializer, CycleSerializer
from rest_framework.decorators import action

class SuperCycleViewSet(viewsets.ModelViewSet):
    """Cycles"""
    permission_classes = [IsManagement]


class CycleViewSet(viewsets.ModelViewSet):
    """Cycles"""
    permission_classes = [IsManagement]
    queryset = Cycle.objects.all()

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
