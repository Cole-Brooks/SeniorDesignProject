from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets
from django.shortcuts import render, redirect
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from .forms import RegistrationForm, Profile, UserForm, LoginForm, UserProfileForm
# from .models import User
# from .serializers import UserSerializer
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()


def user_registration(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            administrator = user.Please_check_this_if_you_are_a_parking_administrator

            if administrator:
                group = Group.objects.get(name='Administrators')
                # Add new user to Administrators group
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Customers')
                # Add new user to Customers group
                user.groups.add(group)
            # Create Profile for new instructor
            Profile.objects.create(user=user)

            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/user_registration.html', {'form': form})


def user_login(request):
    """ Login View for Instructors"""

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(request, password=credentials['password'], username=credentials['username'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    """Custom Log out request"""

    logout(request)
    return render(request, 'account/logout.html')


@login_required
def edit_profile(request):
    """View to edit profile"""
    if request.method == 'POST':
        form = UserForm(instance=request.user, data=request.POST)
        profile_form = UserProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Profile has been successfully updated')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html',
                  {'form': form, 'profile_form': profile_form})
