from random import randint
from django.contrib.auth.hashers import make_password
from django.db import models

# -----
# Will be unused with the removal of Admin
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
)
from django.utils.translation import ugettext_lazy as _

# -------
from phonenumber_field.modelfields import PhoneNumberField

from .choices import *
from tutor_smith.converters import h_encode, user_hasher

from django.utils import timezone

dict_subject = dict(choice_subject)

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
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    password = models.CharField(max_length=265)
    gender = models.IntegerField(choices=choice_gender)
    address = models.CharField(max_length=64, blank=True, null=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def create_default_data(self):
        """
        Creates a default context
        Can be used for resets
        """
        self.email = self.email.lower()
        self.description = ''
        self.is_active = True
        self.is_staff = False
        self.is_admin = False
        self.certificate = None
        self.profile_pic = None
        self.created_on = timezone.now()

    def set_password(self, plainpassword: str):
        """
        sets the password of the model to a hashed and salted password
        """
        self.password = make_password(
            plainpassword,
            salt=str(randint(0, 2 ** 15)),
        )

    def get_hashid(self):
        """
        Returns the id hashed with the user_hasher
        """
        return h_encode(user_hasher, self.id)


class Settings(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_address = models.BooleanField()
    show_phone = models.BooleanField()

    def create_default(self):
        """
        Creates a default context
        Can be used for resets
        """
        self.show_address = False
        self.show_phone = False


class Info(models.Model):
    subject = models.IntegerField(choices=choice_subject)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    level_class = models.IntegerField()
    difficulity = models.IntegerField(choices=choice_difficulity)
    cost_budget = models.DecimalField(max_digits=5, decimal_places=2)
    searching = models.BooleanField()

    created_on = models.DateTimeField()

    def __str__(self):
        return self.author.email + ' ' + str(self.subject)

    def get_hr_subject(self):
        """
        Returns the subject in human readable form
        """
        return dict_subject[self.subject]

    def get_hashid(self):
        """
        Returns the id hashed with the user_hasher
        """
        return h_encode(user_hasher, self.id)


class Review(models.Model):

    title = models.CharField(max_length=24)
    text = models.TextField()
    stars = models.IntegerField()
    author = models.ForeignKey(
        User, related_name='Author', on_delete=models.CASCADE
    )
    for_user = models.ForeignKey(
        User, related_name='for_user', on_delete=models.CASCADE
    )

    created_on = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_hashid(self):
        """
        Returns the id hashed with the user_hasher
        """
        return h_encode(user_hasher, self.id)
