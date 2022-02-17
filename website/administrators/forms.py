# from django import forms
# from django.conf import settings
# from django.db import models
# from users.models import User
# from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget
# from .models import Administrator
#
#
# class AdministratorLoginForm(forms.Form):
#     """Login form to for authentication system"""
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#
# class AdministratorRegistrationForm(forms.ModelForm):
#     """ Parking Administrator Registration Form"""
#     parking_name = forms.CharField(label='Parking Name', max_length=250, required=True, widget=forms.TextInput(
#         attrs={'placeholder': 'Parking Name', 'class': 'form-control'}))
#     phone = PhoneNumberField(label="Phone number", widget=PhoneNumberPrefixWidget(initial='US',
#                                                                                   attrs={'placeholder': 'Phone number',
#                                                                                          'class': 'form'
#                                                                                                   '-control'}),
#                              required=False)
#     password1 = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput(
#         attrs={'placeholder': 'Password', 'class': 'form-control'}))
#     password2 = forms.CharField(label='Repeat Password', min_length=8, required=True, widget=forms.PasswordInput(
#         attrs={'placeholder': 'Repeat Password', 'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
#
#     def clean_password(self):
#         credentials = self.cleaned_data
#         if credentials['password'] != credentials['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return credentials['password2']
#
#
# class UserForm(forms.ModelForm):
#     """User form to allow users to manage their profiles"""
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     photo = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/', blank=True)
#
#     def __str__(self):
#         return f'Profile for user {self.user.username}'
#
#     @property
#     def get_avatar_url(self):
#         if self.photo and hasattr(self.photo, 'url'):
#             return self.photo.url
#         else:
#             return "https://res.cloudinary.com/dh13i9dce/image/upload/v1642216377/media/avatars/defaultprofile_vad1ub.png"
