from django import forms
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from django.db import models
from users.models import User, Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class LoginForm(forms.Form):
    """Login form to for authentication system"""
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'id': 'username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'id': 'password', 'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact=username)

        if not queryset.exists():
            raise forms.ValidationError("Invalid user.")
        return username


class RegistrationForm(forms.ModelForm):
    """ Parking User Registration Form"""
    Please_check_this_if_you_are_a_parking_administrator = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    username = forms.CharField(label='Username', min_length=5, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter password', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', min_length=3, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter first name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', min_length=3, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter last name', 'class': 'form-control'}))

    email = forms.EmailField(label='Email', min_length=5, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email', 'class': 'form-control'}), help_text="We don't share your email.")

    password1 = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
                                help_text="Enter the same password as above.")

    error_messages = {
        'password_mismatch': _("Sorry! The passwords you entered don't match."),
        'password_less_than_eight': _("Password length should not be less than 8 characters"),
    }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'Please_check_this_if_you_are_a_parking_administrator',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_less_than_eight'],
                code='password_less_than_eight',
            )

        return password2


class UserForm(forms.ModelForm):
    """User form to allow users to manage their profiles"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    """User form to allow users to manage their profiles, including their profile photo"""

    class Meta:
        model = Profile
        fields = ('photo',)
