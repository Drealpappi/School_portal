from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.models import TimeStampedUUIDModel
from .managers import CustomUserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimeStampedUUIDModel):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'School Admin'
        TEACHER = 'TEACHER', 'Teacher'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'

    email = models.EmailField(unique=True, db_index=True, max_length=80)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} ({self.role})"

