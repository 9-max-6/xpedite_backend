from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Request
from rest_framework.exceptions import PermissionDenied
from .serializers import RequestSerializerMin, RequestSerializerMax
from .permissions import IsManagement, IsSupervisor

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializerMin

    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()
    
    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action == 'jets':
            # Admin users can retrieve requests
            return [IsSupervisor()]
        if self.action == 'me':
            # Admin users can retrieve requests
            return [IsAuthenticated()]
        if self.action == 'retrieve':
            # Admin users can retrieve requests
            return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        """Override the default retrieve method for additional customization."""
        instance = self.get_object()  # Fetch the object by its primary key (ID)

        # Custom logic: You can perform additional checks or modifications here
        # Example: Check if the request.user is allowed to access this specific request
        if instance.user.id != requst.user.id:
            # check if the user is a supervisor.
            if(not request.user.hasperm(IsManagement)):
                # check if the user is a supervisor for the same region
                if not request.user.designation == 'SUP':
                    # unauthorized
                    raise PermissionDenied('You do not have access to this object')
                if not request.user.region == instance.user.region:
                    # unauthorized
                    raise PermissionDenied('You do not have access to this object')

        # Use the appropriate serializer
        serializer = self.get_serializer(instance)

        # Return the serialized data
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def my_requests(self, request):
        """Filter requests based on the designation of the user who owns the request."""
        # Filter requests where the 'user' (owner) has the 'supervisor' designation
        queryset = Request.objects.filter(user=request.user).order_by('uploaded_at') 
        serializer = self.get_serializer(queryset, many=True)

        # Return the serialized data
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='jets')
    def jets_requests(self, request):
        """Filter requests based on the designation of the user who owns the request."""
        # Filter requests where the 'user' (owner) has the 'supervisor' designation
        queryset = Request.objects.filter(user__region=request.user.region).order_by('uploaded_at')  
        serializer = self.get_serializer(queryset, many=True)

        # Return the serialized data
        return Response(serializer.data)