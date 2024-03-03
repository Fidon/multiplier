from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


@never_cache
def trips_page(request, tp=None):
    context = {
        'trip_info': tp,
    }
    return render(request, 'trips/trips.html', context)
