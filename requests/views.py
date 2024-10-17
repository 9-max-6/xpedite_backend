from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from cycles.models import Cycle
from files.models import File
from .models import Request
from .serializers import RequestSerializerMin, RequestSerializerMax
from .permissions import IsManagement, IsSupervisor

class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'jets', 'approve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """List all the requests for the current supercycle."""
        queryset = Request.objects.filter(supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new request and associate it with a cycle and supercycle."""
        # Ensure a cycle exists for this user and supercycle
        cycle, created = Cycle.objects.get_or_create(user=request.user, supercycle=request.supercycle)

        # Check if a request of the same type already exists for this cycle
        if cycle.requests.filter(type=request.data.get('type')).exists():
            return Response({'detail': 'Request of this type already exists for this cycle.'}, status=400)

        # Handle file creation if file is uploaded
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file:
            # Read the file into bytes
            file_bytes = uploaded_file.read()
            # Now you have the file content as bytes in file_bytes
            file_instance = File.objects.create(file_name=uploaded_file.name, file_content=file_bytes, user=request.user)
        else:
            return Response({'detail': 'No file uploaded.'}, status=400)

        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()

        # Permission check: If the user isn't the owner of the request, perform additional checks
        if instance.user.id != request.user.id:
            if request.user.is_sup and request.user.region == instance.user.region:
                    # Serialize and return the object
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied('You do not have access to this object.')

        # Serialize and return the object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Filter requests based on the user and current supercycle."""
        queryset = Request.objects.filter(user=request.user, supercycle=request.supercycle)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='jets')
    def jets(self, request):
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sup')
    def sup(self, request):
        # This isn't right...the permission needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_sup=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rm')
    def rm(self, request):
        # here the permissions needs to be IsManagement
        """Filter requests for users in the same region as the supervisor."""
        queryset = Request.objects.filter(user__is_rm=True, supercycle=request.supercycle).order_by('uploaded_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods='patch', url_path='approve')
    def approve(self, request):
        """A call to approve the request"""
        current_request = self.get_object()
        if not current_request:
            return Response('Not found', status=404)
        if not request.user.is_sup():
            return Response('Unauthorized', status=401)
            # check if the right supervisor is approving
        if request.user.region != current_request.user.region:
            return Response('Unauthorized', status=401)
            # check if the request is already approved by a user.
        current_request.status == request.POST.get('status')
        current_request.save()
