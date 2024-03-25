from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from .models import Truck_driver, Trailer, Truck
from apps.trips.models import Trip, Trip_history
from .forms import Truck_driverForm, TrailerForm, TruckForm
from utils.util_functions import format_reg, format_phone, format_license
from datetime import datetime
from django.http import JsonResponse
from utils.util_functions import EA_TIMEZONE
from django.db.models import Q
import pytz
# from django.contrib.auth.decorators import login_required

# tanzania/east africa timezone
tz_tzone = EA_TIMEZONE()
format_datetime = "%Y-%m-%d %H:%M:%S.%f"


# trucks page view
@never_cache
def trucks_page(request, truck=None):
    def filter_truck_drivers(driver_id=None):
        if driver_id:
            return Truck_driver.objects.filter(Q(trk_driver__isnull=True) | Q(id=driver_id), deleted=False).order_by('fullname')
        return Truck_driver.objects.filter(trk_driver__isnull=True, deleted=False).order_by('fullname')

    def filter_trailers(trailer_id=None):
        if trailer_id:
            return Trailer.objects.filter(Q(trk_trailer__isnull=True) | Q(id=trailer_id), deleted=False)
        return Trailer.objects.filter(trk_trailer__isnull=True, deleted=False)
    
    if request.method == 'POST' and truck is None:
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Truck.objects.exclude(deleted=True)

        # Date range filtering
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        date_range_filters = Q()
        if start_date:
            start_date = datetime.strptime(start_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__lte=end_date)

        if date_range_filters:
            queryset = queryset.filter(date_range_filters)


        # Base data from queryset
        base_data = []
        for truck in queryset:
            trailer_data = {
                'id': truck.id,
                'regdate': truck.regdate,
                'regnumber': truck.regnumber,
                'type': truck.truckType,
                'horse': truck.horseType,
                'model': truck.truckModel,
                'trailer': truck.trailer.regnumber if truck.trailer else "N/A",
                'driver': truck.driver.fullname if truck.driver else "N/A",
                'status': "Enroute"
            }
            base_data.append(trailer_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'id',
            1: 'regdate',
            2: 'regnumber',
            3: 'type',
            4: 'horse',
            5: 'model',
            6: 'trailer',
            7: 'driver',
            8: 'status'
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'regdate')
        if order_dir == 'asc':
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=False)
        else:
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=True)

        # Apply individual column filtering
        for i in range(len(column_mapping)):
            column_search = request.POST.get(f'columns[{i}][search][value]', '')
            if column_search:
                column_field = column_mapping.get(i)
                if column_field:
                    filtered_base_data = []
                    for item in base_data:
                        column_value = str(item.get(column_field, '')).lower()
                        if column_field == 'horse':
                            if column_search.lower() == column_value:
                                filtered_base_data.append(item)
                        else:
                            if column_search.lower() in column_value:
                                filtered_base_data.append(item)

                    base_data = filtered_base_data

        # Apply global search
        if search_value:
            base_data = [item for item in base_data if any(str(value).lower().find(search_value.lower()) != -1 for value in item.values())]

        # Calculate the total number of records after filtering
        records_filtered = len(base_data)

        # Apply pagination
        base_data = base_data[start:start + length]

        # Calculate row_count based on current page and length
        page_number = start // length + 1
        row_count_start = (page_number - 1) * length + 1


        # Final data to be returned to ajax call
        final_data = []
        for i, item in enumerate(base_data):
            final_data.append({
                'count': row_count_start + i,
                'id': item.get('id'),
                'regdate': item.get('regdate').strftime('%d-%b-%Y'),
                'regnumber': format_reg(item.get('regnumber')),
                'type': item.get('type'),
                'horse': item.get('horse'),
                'model': item.get('model'),
                'trailer': format_reg(item.get('trailer')) if item.get('trailer') != "N/A" else "N/A",
                'driver': item.get('driver'),
                'status': item.get('status'),
                'action': ''
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)
    
    if request.method == 'GET' and truck is not None and Truck.objects.filter(id=truck, deleted=False).exists():
        trk = Truck.objects.get(id=truck)
        truck_trips = Trip.objects.filter(truck=trk)
        truck_trip_history = []

        for count, trip in enumerate(truck_trips, start=1):
            last_status = "N/A"
            if Trip_history.objects.filter(trip=trip).exists():
                h = Trip_history.objects.filter(trip=trip).order_by('-id').first()
                last_status = h.tripstatus
            
            truck_trip_history.append({
                'count': count,
                'triptype': trip.batch.batchType,
                'startdate': trip.startDate.strftime('%d-%b-%Y %H:%M'),
                'destination': trip.destination,
                'laststatus': last_status,
                'complete': 'Yes' if trip.completed else 'No',
                'trip_url': reverse('trip_details', kwargs={'trip_id': trip.id}),
            })

        truck_data = {
            'id': truck,
            'regdate': trk.regdate.strftime('%d-%b-%Y %H:%M:%S'),
            'regby': trk.addedBy.fullname,
            'reg': format_reg(trk.regnumber),
            'type': trk.truckType,
            'horse': trk.horseType,
            'model': trk.truckModel,
            'info': trk.describe if trk.describe else '-',
            'lastEdit': trk.lastEdited.strftime('%d-%b-%Y %H:%M:%S') if trk.lastEdited else 'N/A',
            'editby': trk.editedBy.fullname if trk.editedBy else 'N/A',
            'driver_name': f"{trk.driver.fullname} - {format_phone(trk.driver.phone)}" if trk.driver else 'N/A',
            'driver_id': trk.driver_id if trk.driver else None,
            'trailer_number': format_reg(trk.trailer.regnumber) if trk.trailer else 'N/A',
            'trailer_id': trk.trailer_id if trk.trailer else None,
        }

        trailers_list = [{'id': trl.id, 'type': trl.trailerType, 'regnumber': format_reg(trl.regnumber)} for trl in filter_trailers(truck_data['trailer_id'])]

        context = {
            'truck_info': truck,
            'truck': truck_data,
            'trip_history': truck_trip_history,
            'drivers': filter_truck_drivers(truck_data['driver_id']),
            'trailers': trailers_list
        }
        return render(request, 'fleet/trucks.html', context)
    
    trailers_list = [{'id': trl.id, 'type': trl.trailerType, 'regnumber': format_reg(trl.regnumber)} for trl in filter_trailers()]
    context = {
        'trailers': trailers_list,
        'drivers': filter_truck_drivers(),
    }
    return render(request, 'fleet/trucks.html', context)


# driver actions view
@never_cache
def truck_operations(request):
    if request.method == 'POST':
        truck_id = request.POST.get('truck_id')
        delete_truck = request.POST.get('delete_truck')

        if truck_id is not None and delete_truck is not None:
            try:
                if Trip.objects.filter(truck_id=truck_id).exists():
                    trp = Trip.objects.get(truck_id=truck_id)
                    if trp.completed:
                        trk = Truck.objects.get(id=truck_id)
                        trk.deleted = not trk.deleted
                        trk.save()
                        fdback = {'success': True, 'sms': 'Success'}
                    else:
                        fdback = {'success': False, 'sms': 'This truck is still on trip.'}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        elif truck_id is not None and delete_truck is None:
            try:
                trk_instance = Truck.objects.get(id=truck_id)
                form = TruckForm(request.POST, instance=trk_instance)
                if form.is_valid():
                    trk = form.save(commit=False)
                    trk.editedBy = request.user
                    trk.lastEdited = datetime.now().replace(tzinfo=pytz.UTC)
                    trk.trailer = form.cleaned_data.get('trailer') or None
                    trk.driver = form.cleaned_data.get('driver') or None
                    trk.describe = form.cleaned_data.get('describe') or None
                    trk.save()
                    fdback = {'success': True, 'sms': 'Information updated successfully!'}
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
                print(e)
                fdback = {'success': False, 'sms': 'Operation failed!'}

        else:
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
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        return JsonResponse(fdback)
    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})


# trailers page view
@never_cache
def trailer_page(request, trailer=None):
    if request.method == 'POST' and trailer is None:
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Trailer.objects.exclude(deleted=True)

        # Date range filtering
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        date_range_filters = Q()
        if start_date:
            start_date = datetime.strptime(start_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__lte=end_date)

        if date_range_filters:
            queryset = queryset.filter(date_range_filters)


        # Base data from queryset
        base_data = []
        for trailer in queryset:
            trailer_data = {
                'id': trailer.id,
                'regdate': trailer.regdate,
                'regnumber': trailer.regnumber,
                'type': trailer.trailerType,
                'truck': "N/A",
                'status': "Enroute"
            }
            if trailer.trk_trailer.exists():
                truck = trailer.trk_trailer.first()
                trailer_data['truck'] = truck.regnumber
            base_data.append(trailer_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'id',
            1: 'regdate',
            2: 'regnumber',
            3: 'type',
            4: 'truck',
            5: 'status'
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'regdate')
        if order_dir == 'asc':
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=False)
        else:
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=True)

        # Apply individual column filtering
        for i in range(len(column_mapping)):
            column_search = request.POST.get(f'columns[{i}][search][value]', '')
            if column_search:
                column_field = column_mapping.get(i)
                if column_field:
                    filtered_base_data = []
                    for item in base_data:
                        column_value = str(item.get(column_field, '')).lower()
                        if column_field == 'type':
                            if column_search.lower() == column_value:
                                filtered_base_data.append(item)
                        else:
                            if column_search.lower() in column_value:
                                filtered_base_data.append(item)

                    base_data = filtered_base_data

        # Apply global search
        if search_value:
            base_data = [item for item in base_data if any(str(value).lower().find(search_value.lower()) != -1 for value in item.values())]

        # Calculate the total number of records after filtering
        records_filtered = len(base_data)

        # Apply pagination
        if length < 0:
            length = len(base_data)
        base_data = base_data[start:start + length]

        # Calculate row_count based on current page and length
        page_number = start // length + 1
        row_count_start = (page_number - 1) * length + 1


        # Final data to be returned to ajax call
        final_data = []
        for i, item in enumerate(base_data):
            final_data.append({
                'count': row_count_start + i,
                'id': item.get('id'),
                'regdate': item.get('regdate').strftime('%d-%b-%Y'),
                'regnumber': format_reg(item.get('regnumber')),
                'type': item.get('type'),
                'truck': format_reg(item.get('truck')) if item.get('truck') != "N/A" else "N/A",
                'status': item.get('status'),
                'action': ''
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)
    
    if request.method == 'GET' and trailer is not None and Trailer.objects.filter(id=trailer, deleted=False).exists():
        trl = Trailer.objects.get(id=trailer)

        trailer_trips = Trip.objects.filter(trailer=trl)
        trailer_trip_history = []

        for count, trip in enumerate(trailer_trips, start=1):
            last_status = "N/A"
            if Trip_history.objects.filter(trip=trip).exists():
                h = Trip_history.objects.filter(trip=trip).order_by('-id').first()
                last_status = h.tripstatus
            
            trailer_trip_history.append({
                'count': count,
                'triptype': trip.batch.batchType,
                'startdate': trip.startDate.strftime('%d-%b-%Y %H:%M'),
                'destination': trip.destination,
                'laststatus': last_status,
                'complete': 'Yes' if trip.completed else 'No',
                'trip_url': reverse('trip_details', kwargs={'trip_id': trip.id}),
            })

        trailer_data = {
            'id': trailer,
            'regdate': trl.regdate.strftime('%d-%b-%Y %H:%M:%S'),
            'regby': trl.addedBy.fullname,
            'reg': format_reg(trl.regnumber),
            'type': trl.trailerType,
            'info': trl.describe if trl.describe else '-',
            'lastEdit': trl.lastEdited.strftime('%d-%b-%Y %H:%M:%S') if trl.lastEdited else 'N/A',
            'editby': trl.editedBy.fullname if trl.editedBy else 'N/A',
            'truck_number': None,
            'truck_id': None
        }
        if trl.trk_trailer.exists():
                truck = trl.trk_trailer.first()
                trailer_data['truck_id'] = truck.id
                trailer_data['truck_number'] = format_reg(truck.regnumber)
        context = {
            'trailer_info': trailer,
            'trailer': trailer_data,
            'trip_history': trailer_trip_history,
        }
        return render(request, 'fleet/trailers.html', context)
    return render(request, 'fleet/trailers.html')


# trailers actions view
@never_cache
def trailer_operations(request):
    if request.method == 'POST':
        trailer_id = request.POST.get('trailer_id')
        delete_trailer = request.POST.get('delete_trailer')

        if trailer_id is not None and delete_trailer is not None:
            try:
                if Trip.objects.filter(truck__trailer_id=trailer_id).exists():
                    trp = Trip.objects.get(truck__trailer_id=trailer_id)
                    if trp.completed:
                        trl = Trailer.objects.get(id=trailer_id)
                        trl.deleted = not trl.deleted
                        trl.save()
                        fdback = {'success': True, 'sms': 'Success'}
                    else:
                        fdback = {'success': False, 'sms': 'This trailer is still on trip'}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        elif trailer_id is not None and delete_trailer is None:
            try:
                trl_instance = Trailer.objects.get(id=trailer_id)
                form = TrailerForm(request.POST, instance=trl_instance)
                if form.is_valid():
                    trl = form.save(commit=False)
                    trl.editedBy = request.user
                    trl.lastEdited = datetime.now().replace(tzinfo=pytz.UTC)
                    trl.describe = form.cleaned_data.get('describe') or None
                    trl.save()
                    fdback = {'success': True, 'sms': 'Information updated successfully!'}
                else:
                    errorMsg = "Unknown error."
                    if 'regnumber' in form.errors:
                        errorMsg = form.errors['regnumber'][0]
                    fdback = {'success': False, 'sms': errorMsg}
            except Exception as e:
                print(e)
                fdback = {'success': False, 'sms': 'Operation failed!'}

        else:
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
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        return JsonResponse(fdback)
    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})


# driver page view
@never_cache
def driver_page(request, driver=None):
    if request.method == 'POST' and driver is None:
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Truck_driver.objects.exclude(deleted=True)

        # Date range filtering
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        date_range_filters = Q()
        if start_date:
            start_date = datetime.strptime(start_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(regdate__lte=end_date)

        if date_range_filters:
            queryset = queryset.filter(date_range_filters)


        # Base data from queryset
        base_data = []
        for driver in queryset:
            driver_data = {
                'id': driver.id,
                'regdate': driver.regdate,
                'fullname': driver.fullname,
                'license': driver.licenseNum,
                'phone': driver.phone,
                'truck': "N/A",
                'status': "Enroute"
            }
            if driver.trk_driver.exists():
                truck = driver.trk_driver.first()
                if truck.trailer is None:
                    driver_data['truck'] = f"{truck.regnumber}/--"
                else:
                    driver_data['truck'] = f"{truck.regnumber}/{truck.trailer.regnumber}"
            base_data.append(driver_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'id',
            1: 'regdate',
            2: 'fullname',
            3: 'license',
            4: 'phone',
            5: 'truck',
            6: 'status'
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'fullname')
        if order_dir == 'asc':
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=False)
        else:
            base_data = sorted(base_data, key=lambda x: x[order_column_name], reverse=True)

        # Apply individual column filtering
        for i in range(len(column_mapping)):
            column_search = request.POST.get(f'columns[{i}][search][value]', '')
            if column_search:
                column_field = column_mapping.get(i)
                if column_field:
                    filtered_base_data = []
                    for item in base_data:
                        column_value = str(item.get(column_field, '')).lower()
                        if column_search.lower() in column_value:
                            filtered_base_data.append(item)

                    base_data = filtered_base_data

        # Apply global search
        if search_value:
            base_data = [item for item in base_data if any(str(value).lower().find(search_value.lower()) != -1 for value in item.values())]

        # Calculate the total number of records after filtering
        records_filtered = len(base_data)

        # Apply pagination
        if length < 0:
            length = len(base_data)
        base_data = base_data[start:start + length]

        # Calculate row_count based on current page and length
        page_number = start // length + 1
        row_count_start = (page_number - 1) * length + 1


        # Final data to be returned to ajax call
        final_data = []
        for i, item in enumerate(base_data):
            final_data.append({
                'count': row_count_start + i,
                'id': item.get('id'),
                'regdate': item.get('regdate').strftime('%d-%b-%Y'),
                'fullname': item.get('fullname'),
                'license': format_license(item.get('license')),
                'phone': format_phone(item.get('phone')),
                'truck': item.get('truck'),
                'status': item.get('status'),
                'action': ''
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)
    
    if request.method == 'GET' and driver is not None and Truck_driver.objects.filter(id=driver, deleted=False).exists():
        drv = Truck_driver.objects.get(id=driver)

        driver_trips = Trip.objects.filter(driver=drv)
        driver_trip_history = []

        for count, trip in enumerate(driver_trips, start=1):
            last_status = "N/A"
            if Trip_history.objects.filter(trip=trip).exists():
                h = Trip_history.objects.filter(trip=trip).order_by('-id').first()
                last_status = h.tripstatus
            
            driver_trip_history.append({
                'count': count,
                'triptype': trip.batch.batchType,
                'startdate': trip.startDate.strftime('%d-%b-%Y %H:%M'),
                'destination': trip.destination,
                'laststatus': last_status,
                'complete': 'Yes' if trip.completed else 'No',
                'trip_url': reverse('trip_details', kwargs={'trip_id': trip.id}),
            })

        driver_data = {
            'id': driver,
            'regdate': drv.regdate.strftime('%d-%b-%Y %H:%M:%S'),
            'regby': drv.addedBy.fullname,
            'fullname': drv.fullname,
            'license': format_license(drv.licenseNum),
            'phone': format_phone(drv.phone),
            'info': drv.describe if drv.describe else '-',
            'lastEdit': drv.lastEdited.strftime('%d-%b-%Y %H:%M:%S') if drv.lastEdited else 'N/A',
            'editby': drv.editedBy.fullname if drv.editedBy else 'N/A',
            'truck_number': None,
            'truck_id': None
        }
        if drv.trk_driver.exists():
                truck = drv.trk_driver.first()
                driver_data['truck_id'] = truck.id
                if truck.trailer is None:
                    driver_data['truck_number'] = f"{truck.regnumber}/--"
                else:
                    driver_data['truck_number'] = f"{truck.regnumber}/{truck.trailer.regnumber}"
        context = {
            'driver_info': driver,
            'driver': driver_data,
            'trip_history': driver_trip_history,
        }
        return render(request, 'fleet/drivers.html', context)
    return render(request, 'fleet/drivers.html')


# driver actions view
@never_cache
def driver_operations(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        delete_driver = request.POST.get('delete_driver')

        if driver_id is not None and delete_driver is not None:
            try:
                if Trip.objects.filter(truck__driver_id=driver_id).exists():
                    trp = Trip.objects.get(truck__driver_id=driver_id)
                    if trp.completed:
                        driver = Truck_driver.objects.get(id=driver_id)
                        driver.deleted = not driver.deleted
                        driver.save()
                        fdback = {'success': True, 'sms': 'Success'}
                    else:
                        fdback = {'success': False, 'sms': 'This driver is still on trip'}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}

        elif driver_id is not None and delete_driver is None:
            try:
                drv_instance = Truck_driver.objects.get(id=driver_id)
                form = Truck_driverForm(request.POST, instance=drv_instance)
                if form.is_valid():
                    dr = form.save(commit=False)
                    dr.editedBy = request.user
                    dr.lastEdited = datetime.now().replace(tzinfo=pytz.UTC)
                    dr.describe = form.cleaned_data.get('describe') or None
                    dr.save()
                    fdback = {'success': True, 'sms': 'Information updated successfully!'}
                else:
                    errorMsg = "Unknown error."
                    if 'phone' in form.errors:
                        errorMsg = form.errors['phone'][0]
                    if 'licenseNum' in form.errors:
                        errorMsg = form.errors['licenseNum'][0]
                    fdback = {'success': False, 'sms': errorMsg}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}

        else:
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
                fdback = {'success': False, 'sms': 'Operation failed!'}
        return JsonResponse(fdback)

    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})
