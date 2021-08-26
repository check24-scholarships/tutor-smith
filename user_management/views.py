#HTML Handeling
from django.shortcuts import render, redirect, get_object_or_404
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
from .validators import validate_login, validate_register
from .choices import *

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

dict_gender = dict(choice_gender)

def index(request):
    __context={"users":User.objects.all()}
    return render(request, "index.html", __context)

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
            profile_pic=None,
            created_on=timezone.now()
            )
            # TODO: Create Context
            request.session["user"] = user.id
            messages.add_message(request, messages.SUCCESS, "Nutzer erstellt!")
            return redirect("/login")
    # Displays Form and Context on view when not returned before
    form = UserForm()
    __context['form'] = form
    return render(request, 'register.html', context=__context)

# XXX: DELETE THIS NOT MY JOB
def login(request):
    __context = {"form": None}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if validate_login(request, form):
            # return redirect("/dashboard")
            return HttpResponse("Login!")
    form = LoginForm()
    __context['form'] = form
    return render(request, 'login.html', __context)


def user_profile(request, user_id):
    __context = {'user':None}
    # TODO: use Hashid to hide Primary key
    print(user_id)
    __context['user']= get_object_or_404(User, id=user_id)
    __context['gender']=dict_gender[__context['user'].gender]
    return render(request, "profile.html", __context)
