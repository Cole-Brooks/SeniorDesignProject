from django.contrib import admin
from django.urls import path, include
from administrators import views
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.routers import DefaultRouter

# Customization of django admin
admin.site.site_header = "Smart Park"
admin.site.site_title = "Smart Park's Dashboard"
admin.site.index_title = "Dashboard"


urlpatterns = [

    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('parking/customers/list/', views.ParkingLotCustomersView.as_view(), name='parking_lots_customers_list'),
    path('parking/list/', views.ParkingLotListView.as_view(), name='parking_lots_list'),
    path('search_parking', views.search_parking_lots, name='search_parking_lots'),
    path('manege_search_parking', views.manage_search_parking_lots, name='manage_search_parking_lots'),
    path('parking/list/on_maps/', views.ParkingLotsMapsView.as_view(), name='parking_lots_maps'),
    path('parking/<slug:slug>/', views.ParkingLotDetailView.as_view(), name='parking_lot_detail'),
    path('parking/list/manage', views.ManageParkingLotListView.as_view(), name='manage_parking_lots_list'),
    path('parking/list/manage/<slug:slug>/', views.ManageParkingLotDetailView.as_view(),
         name='manage_parking_lot_detail'),
    path('create/', views.CreateParkingLotView.as_view(), name='parking_create'),
    path('<pk>/edit/', views.UpdateParkingLotView.as_view(), name='parking_edit'),
    path('<pk>/delete/', views.DeleteParkingLotView.as_view(), name='parking_delete'),

]
