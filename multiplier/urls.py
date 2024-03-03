from django.contrib import admin
from django.urls import include, path
from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.login_page, name='auth_url'),
    path('auth/', v.login_page, name='auth_url'),
    path('home/', v.home_page, name='home_url'),

    path('fleet/', include('apps.fleet.urls')),
    path('trips/', include('apps.trips.urls')),
]
