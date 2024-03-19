from django.urls import path
from . import views as v

urlpatterns = [
    path('trucks/', v.trucks_page, name='trucks'),
    path('trucks/<int:truck>/', v.trucks_page, name='truck_details'),
    path('trucks/operations/', v.truck_operations, name='truck_operations'),
    path('trailers/', v.trailer_page, name='trailers'),
    path('trailers/<int:trailer>/', v.trailer_page, name='trailer_details'),
    path('trailers/operations/', v.trailer_operations, name='trailer_operations'),
    path('drivers/', v.driver_page, name='drivers'),
    path('drivers/<int:driver>/', v.driver_page, name='driver_details'),
    path('drivers/operations/', v.driver_operations, name='driver_operations'),
]
