# HTML Handeling
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .forms import *
from .models import User, Info, Review, Settings
from .validators import validate_login, validate_register
from .choices import *
from tutor_smith.utils import get_client_ip, is_user_authenticated

dict_gender = dict(choice_gender)


def index(request):
    __context = {'users': User.objects.all()}
    return render(request, 'index.html', __context)


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
            user = User.objects.get(email=data)
            print(user)
            subject = 'Password Reset Requested'
            email_template_name = 'main/password/password_reset_email.txt'
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


# Handels incoming GET & POST requests on the register view.
def register(request):
    # All context gets initialized
    __context = {'form': None}
    if request.method == 'POST':
        form = UserForm(request.POST)

        res = validate_register(request, form)
        if res:
            user = User(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                address=form.cleaned_data['adress'],
                phone=form.cleaned_data['phone'],
                user_class=form.cleaned_data['user_class'],
                birth_date=form.cleaned_data['birth_date'],
                ip=get_client_ip(request),
            )
            user.set_password(form.cleaned_data['password_1'])
            user.create_default_data()
            user.save()
            user_settings = Settings(user=user)
            user_settings.create_default()
            user_settings.save()
            request.session['user'] = user.id
            messages.add_message(request, messages.SUCCESS, 'Nutzer erstellt!')
            return redirect('/login')
    # Displays Form and Context on view when not returned before
    form = UserForm()
    __context['form'] = form
    return render(request, 'register.html', context=__context)


def login(request):
    try:
        if request.session['userid']:
            return redirect('/')
    except KeyError:
        pass

    __context = {'form': None}
    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            return HttpResponse('Please Enable Cookies')
        request.session.delete_test_cookie()
        form = LoginForm(request.POST)
        user = validate_login(request, form)
        if user:
            request.session['userid'] = user.get_hashid()
            user.ip = get_client_ip(request)
            user.save()
            return redirect('/')

    form = LoginForm()
    __context['form'] = form
    request.session.set_test_cookie()
    return render(request, 'login.html', __context)


def logout(request):
    request.session.flush()
    return HttpResponse("Logged out! <a href=\"/\">Back</a>")


@csrf_exempt
def user_profile(request, user_id, subpath):
    __context = {
        'user': get_object_or_404(User, id=user_id),
        'isOwner': is_user_authenticated(request),
    }
    try:
        __context['settings'] = Settings.objects.get(user=__context['user'])
    except Settings.DoesNotExist:
        return HttpResponseServerError()

    if subpath == 'profile':
        __context['gender'] = dict_gender[__context['user'].gender]
        __context['review'] = (
            Review.objects.filter(for_user=__context['user'])
            .order_by('-stars')
            .first()
        )
        return render(request, 'profile/profile.html', __context)
    elif subpath == 'infos':
        __context['infos'] = Info.objects.filter(author=__context['user'])
        return render(request, 'profile/infos.html', __context)
    elif subpath == 'reviews':
        __context['reviews'] = Review.objects.filter(
            for_user=__context['user']
        )
        return render(request, 'profile/reviews.html', __context)
    elif subpath == 'edit':
        if __context['isOwner']:
            if request.method == 'POST':
                form = ProfileEditForm(
                    request.POST,
                    user=__context['user'],
                    settings=__context['settings'],
                )
                if form.is_valid():
                    __context['user'].description = form.cleaned_data[
                        'description'
                    ]
                    # Change everything
                    __context['user'].save()
                    __context['settings'].show_phone = form.cleaned_data[
                        'show_phone'
                    ]
                    __context['settings'].show_address = form.cleaned_data[
                        'show_address'
                    ]
                    __context['settings'].save()
                    # TODO: Add feedback for saved changes

            __context['form'] = ProfileEditForm(
                user=__context['user'], settings=__context['settings']
            )
            return render(request, 'profile/edit.html', __context)
        else:
            return Http404()
