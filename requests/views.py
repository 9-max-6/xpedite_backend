from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from cycles.models import Cycle
from files.models import File
from .models import Request
from .serializers import RequestSerializerMin, RequestSerializerMax, RequestSerializerMake
from .permissions import IsManagement, IsSupervisor

class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializerMin
    permission_classes = [IsManagement]
    queryset = Request.objects.all()

    def get_serializer_class(self):
        """Use different serializers for specific actions."""
        if self.action == 'retrieve':
            return RequestSerializerMax
        if self.action == 'create':
            return RequestSerializerMake
        return super().get_serializer_class()

    def get_permissions(self):
        """Override to apply different permissions based on action."""
        if self.action in ['jets']:
            return [IsSupervisor()]
        if self.action in ['me', 'create', 'retrieve', 'approve']:
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

        total = request.data.get('total')
        try:
            total = int(total)
        except ValueError:
            return  Response({'detail': 'Total must be integer.'}, status=400)
        # Create the request object
        request_data = {
            'type': request.data.get('type'),
            'description': request.data.get('description'),
            'title': request.data.get('title'),
            'total': total,
            'file': file_instance,
            'cycle': cycle,
            'supercycle': request.supercycle,
            'user': request.user,
        }

        print(request_data)

        request_instance = Request.objects.create(**request_data)

        # Serialize and return the new request
        serializer = self.get_serializer(request_instance)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add permission checks for supervisor and management."""
        instance = self.get_object()
        # Permission check: If the user isn't the owner of the request, perform additional checks
        if not request.user.designation == 'FIN':
            if not request.user.designation == 'STAFF':
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
        queryset = Request.objects.filter(user__region=request.user.region, supercycle=request.supercycle).exclude(user=request.user).order_by('uploaded_at')
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

    @action(detail=True, methods=['patch'], url_path='approve')
    def approve(self, request, *args, **kwargs):
        """overrides the patch method."""
        current_request = self.get_object()
        print('Running update on request')

        print(request.data)
        
        # data in request.data
        # check the user designation
        # if the user is a JET, raise 401
        # if the user is a supervisor
        # check if the user is a supervisor in the same region as the user in request
        # if not, return 403
        # if they are, update the request to reviewed if not already set. -- request status must be posted.
        # if not a supervisor, check if the user is in finance, in which case the request is to be update
        # accordingly.

        # status must be 'approved' or 'rejected'


        status = request.data.get('status')
        comment = request.data.get('comment')

        status_options = ['approve', 'reject']

        flag = False

        if (not status or not comment):
            flag = True
        if not status in status_options:
            flag = True
        

        if flag:

            print(status)
            print(comment)
            return Response('Bad request: layer one', status=400)
            
        
        user = request.user
        if user.designation == 'JET':
            return Response('You are not allowed here buddy', status=401)
        
        # check if they are a supervisor.
        if user.is_sup:
            # login for a supervisor.
            print('Supervisor')
            if not user.is_rm:
                # RC or DRC
                if user.region != current_request.user.region or user.id == current_request.user.id:
                    # bad RC
                    return Response('Run', status=403)
            # user is either RM or supervisor in the same region
            # update
            # check if the request status is posted.

            if not current_request.status == 'posted':
                return Response('Nuh huh huh', 400)

            try:
                reviewed = 'reviewed' if  status == 'approve' else 'rejected_supervisor'
                current_request.status = reviewed
                current_request.comment = comment
                current_request.reviewed_by_sup.add(user)
                current_request.save()
                return Response('Updated successfully', status=201)
            except Exception as e:
                print(e)

        # user is finance
        if user.designation == 'FIN':
            # check if the request is already approved by supervisor
            # check if the request has been approved before
            if current_request.status.endswith('finance') or current_request.status != 'reviewed':
                return Response('Nuh huh huh', 400)
            try:

                reviewed = 'approved_finance' if  status == 'approve' else 'rejected_finance'

                current_request.status = reviewed
                current_request.finance_comment = comment
                current_request.reviewed_by_finance.add(user)
                current_request.save()
                return Response('Updated successfully', status=201)
            except Exception as e:
                print(e)

        # no way you get to this code
        return Response("I'm gonna find you")
