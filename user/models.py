from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='user', default='user/default.png')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'
        permissions = [
            ("assign_user_group_permission",
             "Can assign user to specific group & permission")
        ]

    def __str__(self):
        return self.email