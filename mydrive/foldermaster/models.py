from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser , Group , Permission
from django.utils.translation import gettext_lazy as _





class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')

    def __str__(self):
        return self.name

  

class File(models.Model):
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files' , null=True , blank=True)
    file = models.FileField(upload_to='uploads/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.name
    


