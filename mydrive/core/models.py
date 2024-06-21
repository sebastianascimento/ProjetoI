from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    storage_used = models.BigIntegerField(default=0)

    is_staff_user = models.BooleanField(default=False)
    is_normal_user = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='core_user_groups',  
        related_query_name='user',
        help_text=_('The groups this user belongs to. A user will '
                    'get all permissions granted to each of '
                    'their groups.'),
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='core_user_permissions', 
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username
