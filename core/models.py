from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(null=True, unique=True, verbose_name='Phone Number')
    name = models.CharField(max_length=128, verbose_name='Username')
    email = models.EmailField(_('email address'), null=True)
    firstname = models.CharField(blank=True, max_length=30, verbose_name='first name')
    lastname = models.CharField(blank=True, max_length=128, verbose_name='last name')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name
