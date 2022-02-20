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

    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('parking/list/', views.ParkingLotListView.as_view(), name='parking_lots_list'),
    #path('<slug:slug>/', views.ParkingLotDetailView.as_view(), name='parking_lot_detail'),
    path('parking/list/manage', views.ManageParkingLotListView.as_view(), name='manage_parking_lots_list'),
    path('create/', views.CreateParkingLotView.as_view(), name='parking_create'),
    path('<pk>/edit/', views.UpdateParkingLotView.as_view(), name='parking_edit'),
    path('<pk>/delete/', views.DeleteParkingLotView.as_view(), name='parking_delete'),

]
