# file_app/models.py
from django.db import models
from requests.models import Request 
from users.models import CustomUser

class File(models.Model):
    file_name = models.CharField(max_length=255, blank=False)
    file_content = models.BinaryField(blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # ForeignKey to the Request model
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='files')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')

    # file manager
    def __str__(self):
        return f'{self.file_name} ({self.file_type})'
