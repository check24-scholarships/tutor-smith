from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# User model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'


# Create your models here.
