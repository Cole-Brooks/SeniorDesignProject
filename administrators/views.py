from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from administrators.models import ParkingLot


# # Create your views here.
# class AdministratorRegistrationView(APIView):
#     """View of registration for administrator users in API"""
#     template_name = 'registration/user_registration.html'



def home(request):
    # View for the home page
    return render(request, 'home.html')

