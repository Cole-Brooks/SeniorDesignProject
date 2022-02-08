from django import forms
from django.conf import settings
#from django.contrib.auth.models import User
from django.db import models
from users.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class LoginForm(forms.Form):
    """Login form to for authentication system"""
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}))


class RegistrationForm(forms.ModelForm):
    """ Parking User Registration Form"""
    Please_check_this_if_you_are_a_parking_administrator = forms.BooleanField(required=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    username = forms.CharField(label='Username', min_length=5, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter password', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', min_length=3, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter first name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', min_length=3, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter last name', 'class': 'form-control'}))

    email = forms.EmailField(label='Email', min_length=5, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email', 'class': 'form-control'}))

    password1 = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat Password', min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'Please_check_this_if_you_are_a_parking_administrator',)

    def clean_password(self):
        credentials = self.cleaned_data
        if credentials['password'] != credentials['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(credentials['password']) < 8:
            self._errors['password'] = self.error_class(['Password length should not be less than 8 characters'])
        return credentials['password2']


class UserForm(forms.ModelForm):
    """User form to allow users to manage their profiles"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    @property
    def get_avatar_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "https://res.cloudinary.com/dh13i9dce/image/upload/v1642216377/media/avatars/defaultprofile_vad1ub.png"


class UserProfileForm(forms.ModelForm):
    """User form to allow users to manage their profiles, including their profile photo"""

    class Meta:
        model = Profile
        fields = ('photo',)
