# file_app/models.py
from django.db import models
from users.models import CustomUser

class File(models.Model):
    file_name = models.CharField(max_length=255, blank=False)
    file_content = models.BinaryField(blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files', blank=False)
    # there should be a one-to-one relationship between a file and a request
    # this relationship is defined in the requests.models module

    def __str__(self):
        return f'{self.file_name} ({self.file_type})'
