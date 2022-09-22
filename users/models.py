from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
GENDER_SELECTION = [
    ("Male", "Male"),
    ("Female", "Female"),
]


class NewUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_SELECTION, blank=True, null=True
    )
    is_customer = models.BooleanField(default=False)
    is_tailor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
