from django.contrib.auth.models import AbstractUser, User, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(_('endereço de email'), blank=True, unique=True)
    password = models.CharField(max_length=128, blank=True)
    #required_fields = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set'  # Add a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set'  # Add a unique related_name
    )