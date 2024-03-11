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

@never_cache
def batches_page(request, bt=None):
    context = {
        'batch_info': bt,
    }
    return render(request, 'trips/batches.html', context)

@never_cache
def op_report_page(request):
    return render(request, 'trips/report.html')