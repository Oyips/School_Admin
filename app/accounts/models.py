from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.# accounts/models.py



class User(AbstractUser):
    ROLE_CHOICES = [
        ('platform_admin', 'Platform Admin'),
        ('school_owner', 'School Owner'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.ForeignKey('school_app.School', null=True, blank=True,
                                on_delete=models.CASCADE, related_name='members')