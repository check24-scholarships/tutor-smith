from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .choices import *

# Creates Forms for validation and rendering. The Structure is similar to the Model
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
    address = forms.CharField(
        max_length=64,
        label='Adresse',
        widget=forms.TextInput(attrs={'placeholder': 'Straße, Stadt'}),
        required=False,
    )
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget())
    user_class = forms.IntegerField(
        label='Klasse',
        required=True,
        validators=[MaxValueValidator(12), MinValueValidator(5)],
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
        self.fields['show_email'].initial = self.settings.show_email
        self.fields['description'].initial = self.user.description

    description = forms.CharField(
        label='Beschreibung', widget=forms.Textarea(), required=False
    )
    show_address = forms.BooleanField(label='Adresse Anzeigen', required=False)
    show_phone = forms.BooleanField(
        label='Telefon Nummer Anzeigen', required=False
    )
    show_email = forms.BooleanField(label='Email Anzeigen', required=False)
    profile_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=False,
    )


class InfoEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Enables prefilled Fields
        self.detail = kwargs.pop('detail')
        super(InfoEditForm, self).__init__(*args, **kwargs)

        if self.detail:
            self.fields['subject'].initial = self.detail.subject
            self.fields['description'].initial = self.detail.description
            self.fields['level_class'].initial = self.detail.level_class
            self.fields['difficulty'].initial = self.detail.difficulty
            self.fields['cost_budget'].initial = self.detail.cost_budget
            self.fields['searching'].initial = self.detail.searching

    subject = forms.ChoiceField(choices=choice_subject, required=True)
    description = forms.CharField(widget=forms.Textarea(), required=True)

    level_class = forms.IntegerField(
        required=True, validators=[MaxValueValidator(12), MinValueValidator(5)]
    )
    difficulty = forms.ChoiceField(choices=choice_difficulty, required=False)
    cost_budget = forms.DecimalField(
        max_digits=5, decimal_places=2, required=True
    )
    searching = forms.BooleanField(required=False)


class ReviewEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Enables prefilled Fields
        self.detail = kwargs.pop('detail')
        super(ReviewEditForm, self).__init__(*args, **kwargs)

        if self.detail:
            self.fields['title'].initial = self.detail.title
            self.fields['text'].initial = self.detail.text
            self.fields['stars'].initial = self.detail.stars

    title = forms.CharField(max_length=24, required=True)
    text = forms.CharField(widget=forms.Textarea(), required=True)
    stars = forms.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], required=True
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


class TicketCreateForm(forms.Form):
    title = forms.CharField(max_length=30, required=True)
    text = forms.CharField(widget=forms.Textarea(), required=True)
    ticket_type = forms.ChoiceField(choices=choice_ticket_type, required=True)
