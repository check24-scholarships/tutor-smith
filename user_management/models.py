from random import randint
from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# -----
# Will be unused with the removal of Admin
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
)
from django.utils.translation import ugettext_lazy as _

# -------
from phonenumber_field.modelfields import PhoneNumberField
from stdimage import JPEGField

from .choices import *
from tutor_smith.converters import h_encode, user_hasher

from django.utils import timezone

dict_subject = dict(choice_subject)


def image_pic_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = 'users/image_%s_%s.%s' % (
        instance.__str__(),
        instance.get_hashid(),
        extension,
    )
    return new_filename


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
    phone = PhoneNumberField(null=True, blank=True)
    user_class = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(5)]
    )
    description = models.TextField(default='')
    birth_date = models.DateField()

    created_on = models.DateTimeField()

    ip = models.GenericIPAddressField(blank=True, null=True)
    certificate = models.BinaryField(blank=True, null=True, default=None)
    profile_pic = JPEGField(
        upload_to=image_pic_path,
        blank=True,
        null=True,
        variations={
            'large': (800, 800, True),
            'thumbnail': (100, 100, True),
        },
        delete_orphans=True,
        default=None,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email

    def create_default_data(self):
        """
        Creates a default context
        Can be used for resets
        """
        self.email = self.email.lower()
        self.description = ''
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
    show_email = models.BooleanField(default=False)
    show_address = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)

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

    level_class = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(5)]
    )
    difficulty = models.IntegerField(choices=choice_difficulty)
    cost_budget = models.DecimalField(max_digits=5, decimal_places=2)
    searching = models.BooleanField()
    virtual = models.BooleanField(default=False)

    created_on = models.DateTimeField()

    def __str__(self):
        return self.author.email + '__' + str(self.subject)

    def get_type(self):
        return 'info'

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
    stars = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User, related_name='Author', on_delete=models.CASCADE
    )
    for_user = models.ForeignKey(
        User, related_name='for_user', on_delete=models.CASCADE
    )

    created_on = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_type(self):
        return 'review'

    def get_hashid(self):
        """
        Returns the id hashed with the user_hasher
        """
        return h_encode(user_hasher, self.id)


class Request(models.Model):
    author = models.ForeignKey(
        User, related_name='request_author', on_delete=models.CASCADE
    )
    for_user = models.ForeignKey(
        User, related_name='request_info_author', on_delete=models.CASCADE
    )
    info = models.ForeignKey(
        Info, related_name='info', on_delete=models.CASCADE
    )


class Ticket(models.Model):
    author = models.ForeignKey(
        User, related_name='ticket_author', on_delete=models.CASCADE
    )
    for_user = models.ForeignKey(
        User,
        related_name='ticket_for_user',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=30)
    text = models.TextField()
    ticket_type = models.IntegerField(choices=choice_ticket_type)
    status = models.IntegerField(choices=choice_ticket_status, default=2)

    def get_hashid(self):
        """
        Returns the id hashed with the user_hasher
        """
        return h_encode(user_hasher, self.id)
