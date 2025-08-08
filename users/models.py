
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Custom user model that uses email as the unique identifier instead of username
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Primary field used for authentication
    email = models.EmailField(_('email address'), unique=True)
    # User profile information
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    # Permission fields
    is_staff = models.BooleanField(default=False)  # Controls access to admin site
    is_active = models.BooleanField(default=True)  # Controls whether user can log in
    # Auto-populated field for user creation timestamp
    date_joined = models.DateTimeField(auto_now_add=True)

    # Custom manager that handles user creation
    objects = CustomUserManager()

    # Specifies the field used as the unique identifier
    USERNAME_FIELD = 'email'
    # Additional fields required when creating a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name']  # campos obligatorios aparte del email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    # String representation of the user
    def __str__(self):
        return self.email
