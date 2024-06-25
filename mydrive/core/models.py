from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    storage_used = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"
