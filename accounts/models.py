from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from accounts.manager import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_first_login = models.BooleanField(default=True)
    is_temp_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="by_created")
    updated_on = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="by_updated")

    REQUIRED_FIELDS = ('email',)
    objects = UserManager()

    def __str__(self):
        return self.username, self.email

    def get_full_name(self):
        return "{}, {}", self.first_name, self.last_name


class Profile(models.Model):
    address = models.TextField(max_length=500, null=True)
    phone1 = models.CharField(max_length=10, null=True, blank=True)
    phone2 = models.CharField(max_length=10, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    avatar = models.URLField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'{self.user} - profile'
