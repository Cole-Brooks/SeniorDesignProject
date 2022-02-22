from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.shortcuts import render, redirect
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from .models import Profile
from .forms import RegistrationForm, Profile, UserForm, LoginForm, UserProfileForm


def user_registration(request):

    form = RegistrationForm(request.POST or None)

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('home'))

    if request.method == 'POST':

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            if user.Please_check_this_if_you_are_a_parking_administrator:
                group = Group.objects.get(name='Administrators')
                # Add new user to Administrators group
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Customers')
                # Add new user to Customers group
                user.groups.add(group)
            # Create Profile for new user
            Profile.objects.create(user=user)

            login(request, user)
            messages.success(request, 'Welcome! Your account has been successfully created')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/user_registration.html', {'form': form})


def user_login(request):
    """ Login View for Instructors"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(request, password=credentials['password'], username=credentials['username'])

            if user is not None:
                if user.is_active:
                    # if user.Please_check_this_if_you_are_a_parking_administrator:
                    login(request, user)
                    messages.success(request, "Welcome back!")
                    return redirect('home')
                # if not user.Please_check_this_if_you_are_a_parking_administrator:
                # return redirect('manage_cars_list')
                else:
                    messages.info(request, 'You account has been disabled')
                    return HttpResponse('Disabled account')
            else:
                messages.info(request, 'Your credentials are invalid')
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    """Custom Log out request"""

    logout(request)
    messages.success(request, 'You have successfully logged out from Smart Park')
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
