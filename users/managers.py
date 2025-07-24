from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the user model, using email as a single identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        # Email validation - ensures email is provided
        if not email:
            raise ValueError(_("El email debe estar definido"))
        # Normalize email - converts to lowercase and standardizes format
        email = self.normalize_email(email)
        # Create the user instance with provided data
        user = self.model(email=email, **extra_fields)
        # Set password securely (handles hashing)
        user.set_password(password)
        # Save the user to the database
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set default admin permissions for superuser
        extra_fields.setdefault('is_staff', True)        # Staff status for admin access
        extra_fields.setdefault('is_superuser', True)   # Superuser status for all permissions
        extra_fields.setdefault('is_active', True)      # Active status by default

        # Validation to ensure superuser has staff permission
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuario debe tener is_staff=True.'))
        # Validation to ensure superuser has superuser permission
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuario debe tener is_superuser=True.'))

        # Create superuser by calling the create_user method
        return self.create_user(email, password, **extra_fields)
