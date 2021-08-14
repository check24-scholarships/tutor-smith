#HTML Handeling
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.utils.text import slugify
from django.utils import timezone

#Auth Handler
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password, password_changed
from random import randint

from .forms import *
from .models import User, Info, Review
from .validators import validate_register

# TODO: Write functional Ipgrabber eg. with django-ipware
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello_world_temp(request):
    return render(
        request, 'hello.html', context={'time': timezone.now(), 'ip':get_client_ip(request)}
    )

# Handels incoming GET & POST requests on the register view. 
def register(request):
    #All context gets initialized
    __context = {'form':None}
    if request.method == "POST":
        form = UserForm(request.POST)
        
        res = validate_register(request, form)
        if res:
            user = User.objects.create(
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=make_password(form.cleaned_data['password_1'], salt=str(randint(0, 2**15))),
            gender=form.cleaned_data['gender'],
            adress=form.cleaned_data['adress'],
            phone=form.cleaned_data['phone'],
            user_class=form.cleaned_data['user_class'],
            description='',
            birth_date=form.cleaned_data['birth_date'],
            ip=get_client_ip(request),
            is_active=True,
            is_staff=False,
            is_admin=False,

            certificate=None,
            profile_pic=None
            )
            # TODO: Create Context
            request.session["user"] = user.id
            messages.add_message(request, messages.SUCCESS, "Nutzer erstellt!")
            return redirect("/login")
    # Displays Form and Context on view when not returned before
    form = UserForm()
    __context['form'] = form
    return render(request, 'register.html', context=__context)
