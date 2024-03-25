from django.urls import path
from . import views as v

urlpatterns = [
    path('trips/', v.trips_page, name='trips'),
    path('trips/<int:trip_id>/', v.trips_page, name='trip_details'),
    path('trips/operations/', v.trip_operations, name='trips_operations'),
    path('trips/history/add/', v.add_trip_history, name='trips_history'),
    path('batches/', v.batches_page, name='batches'),
    path('batches/<int:batch_id>/', v.batches_page, name='batch_details'),
    path('batches/operations/', v.batch_operations, name='batches_operations'),
    path('report/', v.op_report_page, name='op_report'),
]
