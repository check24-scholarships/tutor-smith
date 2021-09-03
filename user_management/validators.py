from typing import List
from django.contrib.auth.password_validation import (
    validate_password,
    password_changed,
    ValidationError,
)
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User, Info, Review


def display_errors(request, msg):
    if type(msg) == List:
        for err in msg:
            messages.add_message(request, messages.ERROR, err)
    else:
        messages.add_message(request, messages.ERROR, msg)


def validate_register(request, form):
    if form.is_valid():
        # Checks if email is already in database SELECT * FROM User WHERE email=email
        if User.objects.filter(email=form.cleaned_data['email']):
            display_errors(request, 'User already exists')
            return False
        # Checks if passwords match
        elif (
            form.cleaned_data['password_1'] == form.cleaned_data['password_2']
        ):
            try:
                validate_password(form.cleaned_data['password_1'], user=User)
                return True
            except ValidationError as error:
                display_errors(request, error)
                return False
        else:
            display_errors(request, 'Passwords don\'t match')
            return False
    else:
        display_errors(request, form.errors)
        return False


def validate_login(request, form) -> User:
    if form.is_valid():
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
            if check_password(
                form.cleaned_data['password'],
                user.password,
            ):
                return user
            else:
                display_errors(request, 'Wrong password')
                return None
        except User.DoesNotExist:
            display_errors(request, 'User doesn\'t exist')
            return None
    else:
        display_errors(request, form.errors)
        return None
