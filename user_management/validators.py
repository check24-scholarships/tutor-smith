from typing import List
from django.contrib.auth.password_validation import validate_password, password_changed, ValidationError
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
        #Checks if email is already in database SELECT * FROM User WHERE email=email
        if User.objects.filter(email=form.cleaned_data['email']):
            display_errors(request, 'User already exists')
            return False
        #Checks if passwords match
        elif form.cleaned_data['password_1'] == form.cleaned_data['password_2']:
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

# XXX: DELETE ME
def validate_login(request, form):
    if form.is_valid():
        try:
            if check_password(form.cleaned_data["password"], User.objects.get(email=form.cleaned_data["email"]).password):
                return True
            else:
                display_errors(request, 'Wrong password')
                return False
        except Exception as e:
            display_errors(request, 'No matching User')
            return False
            print(e)
    else:
        display_errors(request, form.errors)
        return False
    