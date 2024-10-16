from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the unique identifier instead of username.
    """
    DESIGNATIONS = [
        ('JET', 'JET'),
        ('DRC', 'DRC'),
        ('RC', 'RC'),
        ('RM', 'RM'),
        ('STAFF', 'STAFF'),
        ('FIN', 'FIN'),
    ]

    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    region = models.CharField(_('region'), max_length=30, blank=False)
    is_jet = models.BooleanField(default=False)
    is_sup = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_rm = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    designation = models.CharField(
        max_length=15,
        choices=DESIGNATIONS,
        default='JET',
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'region', 'designation']

    def __str__(self):
        return self.email
