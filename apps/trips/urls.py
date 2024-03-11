from django.urls import path
from . import views as v

urlpatterns = [
    path('trips/', v.trips_page, name='trips'),
    path('trip/<int:tp>/', v.trips_page, name='trip_details'),
    path('batches/', v.batches_page, name='batches'),
    path('batch/<int:bt>/', v.batches_page, name='batch_details'),
    path('report/', v.op_report_page, name='op_report'),
]
