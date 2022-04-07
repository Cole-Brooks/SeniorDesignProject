from django.contrib import admin
from django.urls import path, include
from customers import views


urlpatterns = [
    path('cars/list/', views.CarListView.as_view(), name='cars_list'),
    path('cars/list/manage/', views.ManageCarListView.as_view(), name='manage_cars_list'),
    path('create/', views.CreateCarView.as_view(), name='car_create'),
    path('<pk>/edit/', views.UpdateCarView.as_view(), name='car_edit'),
    path('<pk>/delete/', views.DeleteCarView.as_view(), name='car_delete'),
    path('<pk>/update_parking/', views.update_car_parking, name='update_car_parking'),
    path('membership/', views.CustomerParkingLotMembershipView.as_view(), name='membership'),
    path('customers/parking_lots/list/', views.CustomerParkingLotView.as_view(), name='customer_parking_lot_list'),
    path('parking_lot/<pk>/', views.CustomerParkingLotDetailView.as_view(), name='customer_parking_lot_details'),

]
