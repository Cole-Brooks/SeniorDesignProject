from django.contrib import admin
from django.urls import path, include
from administrators import views

# Customization of django admin
admin.site.site_header = "Team Cash's Parking"
admin.site.site_title = "Welcome to Team Cash's Dashboard"
admin.site.index_title = "Welcome to the Portal"

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
]
