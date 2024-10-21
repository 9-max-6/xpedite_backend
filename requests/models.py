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
        ('rejected_supervisor', 'Rejected by supervisor'),
        ('approved_finance', 'Approved by Finance'),
        ('rejected_finance', 'Rejected by finance'),
    ]
    type_options = [
        ('A', 'Activity Request'),
        ('P', 'Activity Planner'),
        ('R', 'Expense Return'),
        ('E', 'Expense Claim'),
        ('C', 'Conference Request'),
    ]

    comment = models.CharField(max_length=255)
    finance_comment  = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    description = models.TextField()
    reviewed_by_finance = models.ManyToManyField(
        CustomUser,
        related_name='reviewed_requests_finance',
        blank=True
    )
    reviewed_by_sup = models.ManyToManyField(
        CustomUser,
        related_name='reviewed_requests_sup',
        blank=True
    )
            
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
    title = models.CharField(
        max_length=100,
        
    )
 