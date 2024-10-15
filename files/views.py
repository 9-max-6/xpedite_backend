from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from requests.permissions import IsManagement
from .models import File
from .serializers import FileSerializer

class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsManagement]

    # Override the retrieve method to stream file contents stored in the database
    @action(detail=True, methods=['get'], url_path='bin')
    def stream_file(self, request):
        file_instance = self.get_object()
        if (not file_instance.user_id == request.user.id):
            if (not request.user.is_staff):
                if (request.user.designation not in ['SUPERVISOR', 'STAFF']):
                    return HttpResponse("Unauthorized", status=401)
        # Set the content type based on the file type (optional, depending on your model)
        content_type = 'application/pdf'
        # Create a response with the binary file content
        response = HttpResponse(file_instance.file_content, content_type=content_type)
        
        # Set the Content-Disposition header to handle file download (optional)
        response['Content-Disposition'] = f'attachment; filename="{file_instance.file_name}"'
        
        return response
