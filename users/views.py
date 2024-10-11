from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Custom action to retrieve the current authenticated user
    @action(detail=False, methods=['get'], url_path='me')
    def get_current_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
