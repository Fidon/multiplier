from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


@never_cache
def trucks_page(request, tk=None):
    context = {
        'truck_info': tk,
    }
    return render(request, 'fleet/trucks.html', context)

@never_cache
def trailer_page(request, tr=None):
    context = {
        'trailer_info': tr,
    }
    return render(request, 'fleet/trailers.html', context)

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