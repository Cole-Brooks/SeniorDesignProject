from django.contrib import admin
from django.urls import path, include
from customers import views


# Customization of django admin
admin.site.site_header = "Team Cash's Parking"
admin.site.site_title = "Welcome to Team Cash's Dashboard"
admin.site.index_title = "Welcome to the Portal"

urlpatterns = [
    path('cars/list/', views.CarListView.as_view(), name='cars_list'),
    path('cars/list/manage/', views.ManageCarListView.as_view(), name='manage_cars_list'),
    path('create/', views.CreateCarView.as_view(), name='car_create'),
    path('<pk>/edit/', views.UpdateCarView.as_view(), name='car_edit'),
    path('<pk>/delete/', views.DeleteCarView.as_view(), name='car_delete'),
    path('membership/', views.CustomerParkingLotMembershipView.as_view(), name='membership'),
    path('customers/parking_lots/list/', views.CustomerParkingLotView.as_view(), name='customer_parking_lot_list'),
    path('parking_lot/<pk>/', views.CustomerParkingLotDetailView.as_view(), name='customer_parking_lot_details'),

]
