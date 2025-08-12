from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    def __str__(self):
        return self.username

