from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .choices import *

# Creates an iterable classes dict for rendering
classes = [[i, i] for i in range(5, 13)]

# Creates Forms for validation and rendering. The Structure is simmilar to the Model
class UserForm(forms.Form):
    email = forms.EmailField(
        max_length=255, label='Email Adresse', required=True
    )
    first_name = forms.CharField(label='Vorname', required=True)
    last_name = forms.CharField(label='Nachname', required=True)
    password_1 = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.PasswordInput(),
        label='Password 1',
        required=True,
    )
    password_2 = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.PasswordInput(),
        label='Password 2',
        required=True,
    )
    gender = forms.ChoiceField(
        choices=choice_gender, label='Geschlecht', required=True
    )
    adress = forms.CharField(
        max_length=64,
        label='Adresse',
        widget=forms.TextInput(attrs={'placeholder': 'Straße, Stadt'}),
        required=False,
    )
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget())
    user_class = forms.ChoiceField(
        choices=classes, label='Klasse', required=True
    )
    birth_date = forms.DateField(
        label='Geburtsdatum',
        # Widgets gives the Input field custom Properties
        widget=forms.DateTimeInput(
            attrs={'class': '', 'type': 'date'}, format=['%d/%m/%Y']
        ),
        required=True,
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255, label='Email Adresse', required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(), label='Password', required=True
    )


class ProfileEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Enables prefilled Fields
        self.user = kwargs.pop('user')
        self.settings = kwargs.pop('settings')
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # add args
        self.fields['show_address'].initial = self.settings.show_address
        self.fields['show_phone'].initial = self.settings.show_phone
        self.fields['description'].initial = self.user.description

    description = forms.CharField(
        label='Beschreibung', widget=forms.Textarea(), required=False
    )
    show_address = forms.BooleanField(label='Adresse Anzeigen', required=False)
    show_phone = forms.BooleanField(
        label='Telefon Nummer Anzeigen', required=False
    )


class ResetForm(forms.Form):
    password_1 = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.PasswordInput(),
        label='Password',
        required=True,
    )
    password_2 = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.PasswordInput(),
        label='Repeat Password',
        required=True,
    )
