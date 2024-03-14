from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    address = models.CharField(max_length = 255, null=True)
    phone_number = models.IntegerField(null=True)
