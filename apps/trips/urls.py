from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.trips_page, name='trips'),
    path('tp/<int:tp>/', v.trips_page, name='trip_details'),
]
