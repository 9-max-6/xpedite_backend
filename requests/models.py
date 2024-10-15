from django.db import models
from users.models import CustomUser
from cycles.models import SuperCycle, Cycle
from files.models import File

# Create your models here.
class Request(models.Model):
    """Request model"""
    status_options = [
        ('posted', 'Submitted by JET'),
        ('reviewed', 'Submitted by Supervisor'),
        ('approved_finance', 'Approved by Finance'),
        ('approved_supervisor', 'Approvided by Supervisor'),
        ('rejected_finance', 'Rejected by finance'),
        ('rejected_supervisor', 'Rejected by supervisor'),
    ]
    type_options = [
        ('A', 'Activity Request'),
        ('R', 'Expense Return'),
        ('E', 'Expense Claim'),
        ('C', 'Conference Request'),
    ]

    comment = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='reviewer', null=True, blank=True)
    status = models.CharField(
        max_length=75,
        choices=status_options,
        default='posted',
    )
    file = models.OneToOneField(File, on_delete=models.CASCADE, related_name='request', null=True, blank=True)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='requests')
    supercycle = models.ForeignKey(SuperCycle, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    type  = models.CharField(
        max_length=75,
        choices=status_options,
        blank=False
    )
