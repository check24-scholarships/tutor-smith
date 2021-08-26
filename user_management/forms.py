from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .choices import *

classes = [[i, i] for i in range(5, 13)]

#Creates Forms for validation and rendering. The Structure is simmilar to the Model
class UserForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label='Email Adresse',
        required=True
    )
    first_name = forms.CharField(label='Vorname', required=True)
    last_name = forms.CharField(label='Nachname', required=True)
    password_1 = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput(), label='Password 1', required=True)
    password_2 = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput(), label='Password 2', required=True)
    gender = forms.ChoiceField(choices=choice_gender, label='Geschlecht', required=True)
    adress = forms.CharField(max_length=64, label='Adresse', required=False)
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget())
    user_class = forms.ChoiceField(choices=classes, label='Klasse', required=True)
    birth_date = forms.DateField(label='Geburtsdatum',
        #Widgets gives the Input field custom Properties
        widget=forms.DateTimeInput(attrs={
            'class': '',
            'type':'date'
            }, format=['%d/%m/%Y']), required=True)

# XXX: DELETE ME
class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label="Email Adresse",
        required=True
    )
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)