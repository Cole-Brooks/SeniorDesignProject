# from abc import ABC
#
# from django.contrib.auth.models import Group
#
# from users.models import User
# from rest_framework import serializers
# from django import forms
# from allauth.account import adapter
# from drf_braces.serializers.form_serializer import FormSerializer
# from rest_framework import serializers
#
# from rest_auth.registration.serializers import RegisterSerializer
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.password_validation import validate_password
#
#
# class UserSerializer(serializers.ModelSerializer):
#     """ Provides serializations for User model instances"""
#
#     class Meta:
#         model = User
#         fields = ('email', 'username','first_name', 'last_name', 'password', 'parking_administrator')
#
#
# class CustomRegisterSerializer(RegisterSerializer):
#     """ Provides serializations for User Registration"""
#     first_name = serializers.CharField(required=True, write_only=True)
#     last_name = serializers.CharField(required=True, write_only=True)
#     parking_administrator = serializers.BooleanField(default=False)
#
#     USER_TYPES = (
#         ('Parking Administrator', 'Parking Administrator'),
#         ('Customer', 'Customer'),)
#     # user_type = serializers.ChoiceField(choices=USER_TYPES, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username','first_name', 'last_name', 'password', 'parking_administrator')
#
#     # Function that cleans data before saving them
#     def get_cleaned_data(self):
#         return {
#             'username': self.validated_data.get('username', ''),
#             'first_name': self.validated_data.get('first_name', ''),
#             'last_name': self.validated_data.get('last_name', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'password2': self.validated_data.get('password2', ''),
#             'email': self.validated_data.get('email', ''),
#             'parking_administrator': self.validated_data.get('parking_administrator', ''),
#
#
#         }
#
#     # Function that saves user's data to database
#     def save(self, request):
#
#         user = adapter.get_adapter().new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         user.parking_administrator = self.cleaned_data.get('parking_administrator')
#         administrators = Group.objects.get(name='Administrators')
#         customers = Group.objects.get(name='Customers')
#         adapter.get_adapter().save_user(request, user, self)
#         user.save()
#         if user.parking_administrator:
#             user.groups.add(administrators)
#         else:
#             user.groups.add(customers)
#         return user
#
#
# class TokenSerializer(serializers.ModelSerializer):
#     """ Provides serializations for User Token to use in API"""
#     user_group = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Token
#         fields = ('key', 'user', 'user_group')
#
#     def get_user_group(self, obj):
#         data = UserSerializer(obj.user).data
#         parking_administrator = data.get('parking_administrator')
#
#         return {
#             'parking_administrator': parking_administrator,
#         }
