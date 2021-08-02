from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.db.models.fields.related import ForeignKey

from .choices import *


#User model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.SlugField()
    adress = models.CharField(max_length=64, blank=True,  null=True)
    user_class = models.IntegerField()
    description = models.TextField()

    created_on = models.DateTimeField()

    ip = models.GenericIPAddressField(blank=True, null=True)
    certificate = models.BinaryField(blank=True, null=True)
    profile_pic = models.BinaryField(blank=True, null=True)

    USERNAME_FIELD='email'

    objects = UserManager()

       

# Create your models here.
class Info(models.Model):
    subject = models.CharField(max_length=20, choices=choice_subject)
    description = models.TextField()
    author = ForeignKey(User, on_delete=models.CASCADE)

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
