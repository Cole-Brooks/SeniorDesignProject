from django.contrib import admin
from django.urls import path, include
from administrators import views
from django.views.generic import TemplateView

# Customization of django admin
admin.site.site_header = "Team Cash's Parking"
admin.site.site_title = "Welcome to Team Cash's Dashboard"
admin.site.index_title = "Welcome to the Portal"

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    #path('home/', views.home, name='home'),
]
