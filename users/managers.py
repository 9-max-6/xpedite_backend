from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email, first_name, last_name, region, and designation."""
        if not email:
            raise ValueError('The Email field must be set')
        if not extra_fields.get('first_name'):
            raise ValueError('The First Name field must be set')
        if not extra_fields.get('last_name'):
            raise ValueError('The Last Name field must be set')
        if not extra_fields.get('region'):
            raise ValueError('The Region field must be set')
        if not extra_fields.get('designation'):
            raise ValueError('The Designation field must be set')

        # Set specific roles based on designation
        designation = extra_fields.get('designation')
        role_flags = {
            'JET': 'is_jet',
            'RM': 'is_rm',
            'DRC': 'is_sup',
            'RC': 'is_sup',
        }
        if designation in role_flags:
            extra_fields[role_flags[designation]] = True

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email, first_name, last_name, region, and designation."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
