from django.db import models
from users.models import CustomUser


# Create your models here.
class SuperCycle(models.Model):
    """super cycle"""
    id = models.UUIDField(primary_key=True)
    created_at = models.TimeField(auto_now=True)


class Cycle(models.Model):
    """cycle"""
    id = models.UUIDField(primary_key=True)
    created_at = models.TimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cycles')
    supercycle = models.ForeignKey(SuperCycle, on_delete=models.CASCADE, related_name='cycles')
    status = models.BooleanField(default=False)
