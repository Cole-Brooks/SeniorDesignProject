from django.contrib import admin
from django.urls import path, include
from users import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.routers import DefaultRouter

# app_name = 'users'
# # Build url dynamically using router
# router = routers.DefaultRouter()
# router.register(app_name, views.UserViewSet)
#
# urlpatterns = router.urls

# Patterns of different paths
urlpatterns = [

    path('accounts/register/', views.user_registration, name='user_registration'),
    path('', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('accounts/login/', views.user_login, name='login'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('due_bills/', views.ManageBillsView.as_view(), name='due_bills'),
    path('paid_bills/', views.PaidBillsView.as_view(), name='paid_bills'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('successful_payement/', views.successful_payment, name='successful_payment'),
    path('cancel_payment/', views.cancel_payment, name='cancel_payment'),

]
