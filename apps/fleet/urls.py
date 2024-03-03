from django.urls import path
from . import views as v

urlpatterns = [
    path('trucks/', v.trucks_page, name='trucks'),
    path('trucks/tk/<int:tk>/', v.trucks_page, name='truck_details'),
    path('trailers/', v.trailer_page, name='trailers'),
    path('trailers/tr/<int:tr>/', v.trailer_page, name='trailer_details'),
    path('permits/', v.permits_page, name='permits'),
    path('permits/p/<int:p>/', v.permits_page, name='permit_details'),
    path('maintenance/', v.maintenance_page, name='maintenance'),
    path('maintenance/m/<int:m>/', v.maintenance_page, name='maintenance_details'),
]
