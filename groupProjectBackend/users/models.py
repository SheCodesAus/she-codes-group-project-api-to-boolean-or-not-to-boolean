from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.db import models


class SheCodesUser(AbstractUser):
    avatar = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    social_link = models.URLField(null=True, blank=True)
    # Authentication Levels:
    is_approver = models.BooleanField(default=False)
    is_shecodes_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
