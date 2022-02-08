from django.contrib import admin
from django.urls import path, include
from administrators import views
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.routers import DefaultRouter


# Customization of django admin
admin.site.site_header = "Team Cash's Parking"
admin.site.site_title = "Welcome to Team Cash's Dashboard"
admin.site.index_title = "Welcome to the Portal"



urlpatterns = [

    #path('', include('django.contrib.auth.urls')),

]