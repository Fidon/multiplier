from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.utils import timezone
import datetime
import pytz
# from django.contrib.auth.decorators import login_required


@never_cache
def trucks_page(request, tk=None):
    context = {
        'truck_info': tk,
    }
    return render(request, 'fleet/trucks.html', context)

@never_cache
def trailer_page(request, tr=None):
    curr1 = datetime.datetime.now()
    curr2 = timezone.make_aware(curr1)
    curr3 = pytz.timezone('Etc/GMT-3')
    # print(f"Timezone name: {timezone.get_current_timezone()}")
    # print(f"Actual datetime: {curr3.localize(curr1)}")
    # print(f"Timezone time: {timezone.now()}")
    context = {
        'trailer_info': tr,
        'dtime': f"{datetime.datetime.now()}",
        'tzname': f"{timezone.get_current_timezone()}",
        'tznow': f"{timezone.now()}",
        'gmt': f"{curr3.localize(curr1)}"
    }
    return render(request, 'fleet/trailers.html', context)

@never_cache
def driver_page(request, d=None):
    context = {
        'driver_info': d,
    }
    return render(request, 'fleet/drivers.html', context)

@never_cache
def permits_page(request, p=None):
    context = {
        'permit_info': p,
    }
    return render(request, 'fleet/permits.html', context)

@never_cache
def maintenance_page(request, m=None):
    context = {
        'maintenance_info': m,
    }
    return render(request, 'fleet/maintenance.html', context)