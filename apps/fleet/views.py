from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .models import Trailer, Truck_driver
from .forms import TrailerForm, Truck_driverForm, TruckForm
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


def format_reg(regnumber):
    return f"{regnumber[:1]} {regnumber[1:4]} {regnumber[4:]}"


# trucks page view
@never_cache
def trucks_page(request, tk=None):
    trailers = Trailer.objects.filter(trk_trailer__isnull=True).exclude(deleted=True)
    trailers_list = [{'id': trl.id, 'type':trl.trailerType, 'regnumber': format_reg(trl.regnumber)} for trl in trailers]
    drivers = Truck_driver.objects.filter(trk_driver__isnull=True).exclude(deleted=True)
    context = {
        'truck_info': tk,
        'trailers': trailers_list,
        'drivers': drivers
    }
    return render(request, 'fleet/trucks.html', context)


# driver actions view
@never_cache
def truck_actions(request):
    fdback = {'success': False, 'sms': 'Invalid method'}
    if request.method == 'POST':
        try:
            form = TruckForm(request.POST)
            if form.is_valid():
                truck = form.save(commit=False)
                truck.addedBy = request.user
                truck.save()
                fdback = {'success': True, 'sms': 'New truck added successfully!'}
            else:
                errorMsg = "Unknown error."
                if 'driver' in form.errors:
                    errorMsg = form.errors['driver'][0]
                if 'trailer' in form.errors:
                    errorMsg = form.errors['trailer'][0]
                if 'regnumber' in form.errors:
                    errorMsg = form.errors['regnumber'][0]
                fdback = {'success': False, 'sms': errorMsg}
        except Exception as e:
            fdback = {'success': False, 'sms': 'Unknown error!'}
    return JsonResponse(fdback)


# trailers page view
@never_cache
def trailer_page(request, tr=None):
    context = {
        'trailer_info': tr
    }
    return render(request, 'fleet/trailers.html', context)


# trailers actions view
@never_cache
def trailer_actions(request):
    fdback = {'success': False, 'sms': 'Invalid method'}
    if request.method == 'POST':
        try:
            form = TrailerForm(request.POST)
            if form.is_valid():
                trailer = form.save(commit=False)
                trailer.addedBy = request.user
                trailer.save()
                fdback = {'success': True, 'sms': 'New trailer added successfully!'}
            else:
                errorMsg = "Unknown error."
                if 'regnumber' in form.errors:
                    errorMsg = form.errors['regnumber'][0]
                fdback = {'success': False, 'sms': errorMsg}
        except Exception as e:
            fdback = {'success': False, 'sms': 'Unknown error!'}
    return JsonResponse(fdback)


# driver page view
@never_cache
def driver_page(request, d=None):
    context = {
        'driver_info': d,
    }
    return render(request, 'fleet/drivers.html', context)


# driver actions view
@never_cache
def driver_actions(request):
    fdback = {'success': False, 'sms': 'Invalid method'}
    if request.method == 'POST':
        try:
            form = Truck_driverForm(request.POST)
            if form.is_valid():
                dr = form.save(commit=False)
                dr.addedBy = request.user
                dr.save()
                fdback = {'success': True, 'sms': 'New driver added successfully!'}
            else:
                errorMsg = "Unknown error."
                if 'phone' in form.errors:
                    errorMsg = form.errors['phone'][0]
                if 'licenseNum' in form.errors:
                    errorMsg = form.errors['licenseNum'][0]
                fdback = {'success': False, 'sms': errorMsg}
        except Exception as e:
            print(e)
            fdback = {'success': False, 'sms': 'Unknown error!'}
            
    return JsonResponse(fdback)



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