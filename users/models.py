from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class NewUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_tailor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
