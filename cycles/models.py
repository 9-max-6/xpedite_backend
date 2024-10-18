import uuid
from django.db import models
from users.models import CustomUser

# Create your models here.
class SuperCycle(models.Model):
    """super cycle"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=255)


class Cycle(models.Model):
    """cycle"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cycles')
    supercycle = models.ForeignKey(SuperCycle, on_delete=models.CASCADE, related_name='cycles')
    status = models.BooleanField(default=False)
