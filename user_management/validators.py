from django.contrib import messages
from django.contrib.auth.password_validation import (
    validate_password,
    ValidationError,
)
from django.contrib.auth.hashers import check_password
from tutor_smith.utils import display_messages
from .models import User


def validate_register(request, form):
    if form.is_valid():
        # Checks if email is already in database SELECT * FROM User WHERE email=email
        if User.objects.filter(email=form.cleaned_data['email'].lower()):
            display_messages(request, 'User already exists', messages.ERROR)
            return False
        # Checks if passwords match
        elif (
            form.cleaned_data['password_1'] == form.cleaned_data['password_2']
        ):
            try:
                validate_password(form.cleaned_data['password_1'], user=User)
                return True
            except ValidationError as error:
                display_messages(request, error, messages.ERROR)
                return False
        else:
            display_messages(request, 'Passwords don\'t match', messages.ERROR)
            return False
    else:
        display_messages(request, form.errors, messages.ERROR)
        return False


def validate_login(request, form) -> User:
    if form.is_valid():
        try:
            user = User.objects.get(email=form.cleaned_data['email'].lower())
            print(form.cleaned_data['password'])
            print(user.password)
            if check_password(
                form.cleaned_data['password'],
                user.password,
            ):
                return user
            else:
                display_messages(request, 'Wrong password', messages.ERROR)
                return None
        except User.DoesNotExist:
            display_messages(request, 'User doesn\'t exist', messages.ERROR)
            return None
    else:
        display_messages(request, form.errors, messages.ERROR)
        return None


def validate_recover(request, form):
    if form.is_valid():
        # Checks if passwords match
        if form.cleaned_data['password_1'] == form.cleaned_data['password_2']:
            try:
                validate_password(form.cleaned_data['password_1'], user=User)
                return True
            except ValidationError as error:
                display_messages(request, error, messages.ERROR)
                return False
        else:
            display_messages(request, 'Passwords don\'t match', messages.ERROR)
            return False
    else:
        display_messages(request, form.errors, messages.ERROR)
        return False
