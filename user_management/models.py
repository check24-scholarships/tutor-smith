from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AbstractUser,
)
from django.utils.translation import ugettext_lazy as _

from .choices import *


# User model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('created_on', timezone.now())
        # extra_fields.setdefault('birth_date', timezone.now())

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


'''
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.SlugField()
    adress = models.CharField(max_length=64, blank=True,  null=True)
    user_class = models.IntegerField(default=11)
    description = models.TextField(default="")
    birth_date = models.DateField()

    created_on = models.DateTimeField()

    ip = models.GenericIPAddressField(blank=True, null=True)
    certificate = models.BinaryField(blank=True, null=True)
    profile_pic = models.BinaryField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD='email'

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
'''


class UserAuth(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


# Create your models here.
class User(models.Model):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.SlugField()
    adress = models.CharField(max_length=64, blank=True, null=True)
    user_class = models.IntegerField(default=11)
    description = models.TextField(default='')
    birth_date = models.DateField()

    created_on = models.DateTimeField()

    ip = models.GenericIPAddressField(blank=True, null=True)
    certificate = models.BinaryField(blank=True, null=True)
    profile_pic = models.BinaryField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email


class Info(models.Model):
    subject = models.CharField(max_length=20, choices=choice_subject)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    level_class = models.IntegerField()
    difficulity = models.IntegerField(choices=choice_difficulity)
    cost_budget = models.FloatField()
    searching = models.BooleanField()

    created_on = models.DateTimeField()

    def __str__(self) -> str:
        return self.subject + self.author


class Review(models.Model):

    title = models.CharField(max_length=24)
    text = models.TextField()
    stars = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    for_user = models.ForeignKey(Info, on_delete=models.CASCADE)

    created_on = models.DateTimeField()

    def __str__(self):
        return self.title
