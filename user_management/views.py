from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils import timezone
import hashlib
import datetime
import re

from .choices import *
from .forms import *
from .models import *

# password_validator = r''

# TODO: Write functional Ipgrabber eg. with django-ipware
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello_world_temp(request):
    return render(
        request, 'hello.html', context={'time': datetime.datetime.now(), 'ip':get_client_ip(request)}
    )

# Handels incoming GET & POST requests on the register view. 
def register(request):
    #All context gets initialized
    __context = {'form':None, 'error_msg':None}
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            #Checks if email is already in database SELECT * FROM User WHERE email=email
            if User.objects.all().filter(email=form.cleaned_data['email']):
                __context['error_msg'] = 'User already exists'
            #Checks if passwords match
            elif form.cleaned_data['password_1'] != form.cleaned_data['password_2']:
                __context['error_msg'] = 'Passwords don\'t match'
            #create new User in database and saves it with user.save()
            else:
                user = User(
                email=form.cleaned_data['email'],
                name=slugify(form.cleaned_data['name']),
                password=hashlib.sha256(form.cleaned_data['password_1'].encode()).hexdigest(),
                gender=form.cleaned_data['gender'],
                adress=form.cleaned_data['adress'],
                user_class=form.cleaned_data['user_class'],
                description='',
                birth_date=form.cleaned_data['birth_date'],
                created_on=timezone.now(),
                ip=get_client_ip(request),
                is_active=True,
                is_staff=False,
                is_admin=False,

                certificate=None,
                profile_pic=None
                )
                user.save()
                return HttpResponse("Valid!")
        else:
            __context['error_msg']="Form is invalide"
    # Displays Form and Context on view when not returned before
    form = UserForm()
    __context['form'] = form
    return render(request, 'register.html', context=__context)