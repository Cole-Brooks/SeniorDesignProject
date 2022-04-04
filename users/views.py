import datetime
import uuid
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from customers.models import ParkingHistory
from .models import Profile
from .forms import RegistrationForm, Profile, UserForm, LoginForm, UserProfileForm
from paypal.standard.forms import PayPalPaymentsForm
from users.models import User


class ManageBillsView(generic.TemplateView, LoginRequiredMixin):
    """View for the first page of the resume"""
    template_name = "customers/payment/bills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bills = ParkingHistory.objects.filter(paid=False).select_related('car').filter(car__owner=self.request.user)
        context["bills"] = bills

        return context


class PaidBillsView(generic.TemplateView, LoginRequiredMixin):
    """View for the first page of the resume"""
    template_name = "customers/payment/paid_bills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bills = ParkingHistory.objects.filter(paid=True).select_related('car').filter(car__owner=self.request.user)
        context["bills"] = bills

        return context


@login_required
def make_payment(request):
    """View for processing payments"""

    amount = ParkingHistory.objects.filter(paid=False).select_related('car').filter(car__owner=request.user).first().get_parking_fee
    receiver = ParkingHistory.objects.filter(paid=False).select_related('car', 'parking').filter(car__owner=request.user).first().get_business_email

    paypal = {
        'business': receiver,
        'amount': amount,
        'item_name': 'Parking payment',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{request.get_host()}{reverse("paypal-ipn")}',
        'return_url': f'http://{request.get_host()}{reverse("successful_payment")}',
        'cancel_return': f'http://{request.get_host()}{reverse("cancel_payment")}',
    }
    form = PayPalPaymentsForm(initial=paypal)

    return render(request, 'customers/payment/payment.html', {'form': form})


@csrf_exempt
def successful_payment(request):
    """View for payments that have been made"""
    parking_history = ParkingHistory.objects.filter(paid=False).select_related('car').filter(
        car__owner=request.user).first()

    user = User.objects.get(pk=request.user.id)
    # Update new balance for the user
    user.balance_due = user.balance_due - parking_history.parking_fee
    user.save()
    parking_history.paid = True
    # Update parking fee for paid bill
    parking_history.parking_fee = 0.00
    parking_history.save()
    # Update payment date
    parking_history.paid_on = datetime.datetime.now
    parking_history.save()
    messages.success(request, "Your payment has successfully been made!")
    return redirect('home')


@csrf_exempt
def cancel_payment(request):
    """View for payments that have been canceled"""
    messages.error(request, "Your payment has been cancelled!")
    return redirect('home')


def user_registration(request):
    """View for user registration"""
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
            else:
                messages.info(request, 'Your credentials are invalid')

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

