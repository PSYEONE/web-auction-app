from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    date_of_birth = models.DateField(null=True, blank=True)

    profile_image = models.ImageField(upload_to="images", null=True, blank=True)
    pass

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Page view count: {self.count}"
