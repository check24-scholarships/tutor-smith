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

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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

 
def recover_form(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            # Send email...
            print(data)
            """associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:"""
            # get users
            users = User.objects.filter(email=data)
            if users is not None:
                for user in users:
                    print(user)
                    subject = 'Password Reset Requested'
                    email_template_name = (
                        'main/password/password_reset_email.txt'
                    )
                    """c = {
                        "email": "test@gmail.com",
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": "test",
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }"""
            # email = render_to_string(email_template_name, c)
            return redirect('/password_reset/done/')

    password_reset_form = PasswordResetForm()
    return render(
        request,
        'password/password_reset_form.html',
        context={'password_reset_form': password_reset_form},
    )


def recover_form_sent(request):
    return render(request, 'password/password_reset_sent.html')


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

'''
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
'''

def user_profile(request, user_id, subpath):
    __context = {'user':get_object_or_404(User, id=user_id) , 'isOwner': True}
    if subpath == 'profile':
        __context['gender']=dict_gender[__context['user'].gender]
        return render(request, "profile/profile.html", __context)
    elif subpath == 'infos':
        __context['infos'] = Info.objects.filter(author=__context['user'])
        return render(request, 'profile/infos.html', __context)
