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
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    storage_used = models.BigIntegerField(default=0)

    # Defina related_name exclusivos para evitar conflitos com auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='foldermaster_user_groups',  # related_name exclusivo para foldermaster.User
        related_query_name='user',
        help_text=_('The groups this user belongs to. A user will '
                    'get all permissions granted to each of '
                    'their groups.'),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='foldermaster_user_permissions',  # related_name exclusivo para foldermaster.User
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )