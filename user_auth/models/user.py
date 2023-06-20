from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User as UserMain
from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseUser(AbstractUser):

    email = models.EmailField(_('endereço de e-mail'), blank=True, unique=True)
    ppassword_confirmation = models.CharField(max_length=100, default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


BaseUser._meta.get_field('username')._unique = False