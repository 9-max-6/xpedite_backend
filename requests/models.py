from django.db import models
from users.models import CustomUser

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

    types_options = [
            ('activity_request', 'Activity Request'),
            ('expense_return]', 'Expense Return'),
            ('expense_claim]', 'Expense Claim'),
    ]
      
    id = models.UUIDField(primary_key=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Foreign Keys
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    
    # status
    status = models.CharField(
        max_length=75,
        choices=status_options,
        default='posted',
    )

    # type
    type = models.CharField(
        max_length=75,
        choices=types_options,
        blank=False
    )

    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer')

class Comments(models.Model):
    """the comments table"""

    id = models.UUIDField(primary_key=True)

    # related to this request
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=False)