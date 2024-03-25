from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from apps.fleet.models import Truck
from .models import Batch, Trip, Trip_history
from .forms import BatchForm, TripForm, Trip_historyForm
from utils.util_functions import format_reg, format_phone
from datetime import datetime
from django.http import JsonResponse
from utils.util_functions import EA_TIMEZONE
from django.db.models import Q
import pytz
# from django.contrib.auth.decorators import login_required


# tanzania/east africa timezone
tz_tzone = EA_TIMEZONE()
format_datetime = "%Y-%m-%d %H:%M:%S.%f"


@never_cache
def trips_page(request, trip_id=None):
    batches_list = Batch.objects.filter(deleted=False)
    trucks = Truck.objects.filter(deleted=False)
    trucks_list = []

    if request.method == 'POST' and trip_id is None:
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Trip.objects.exclude(deleted=True)

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
        for trp in queryset:
            today_date = trp.completeDate if trp.completeDate else datetime.now(pytz.UTC)
            days_taken = (today_date.date() - trp.startDate.date()).days

            trip_status = "N/A"
            trip_position = "N/A"
            if Trip_history.objects.filter(trip_id=trp.id, deleted=False).exists():
                history = Trip_history.objects.filter(trip_id=trp.id, deleted=False).order_by('-id').first()
                trip_status = history.tripstatus
                trip_position = history.newposition

            trip_data = {
                'id': trp.id,
                'regdate': trp.regdate,
                'batch': trp.batch.batchnumber,
                'batch_id': trp.batch_id,
                'truck': f"{format_reg(trp.truck.regnumber)}/{format_reg(trp.truck.trailer.regnumber)}" if trp.truck.trailer else f"{format_reg(trp.truck.regnumber)}/-N/A",
                'truck_id': trp.truck_id,
                'driver': trp.truck.driver.fullname,
                'driver_id': trp.truck.driver_id,
                'startdate': trp.startDate,
                'status': trip_status,
                'currentposition': trip_position,
                'type': trp.batch.batchType,
                'days': 0 if days_taken <= 0 else days_taken,
                'complete': "Yes" if trp.completed else "No"
            }
            base_data.append(trip_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'id',
            1: 'batch',
            2: 'truck',
            3: 'driver',
            4: 'startdate',
            5: 'status',
            6: 'currentposition',
            7: 'type',
            8: 'days',
            9: 'complete'
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'startdate')
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
                        if column_field in ('type', 'complete'):
                            if column_search.lower() == column_value:
                                filtered_base_data.append(item)
                        elif column_field == 'days':
                            if column_search.startswith('-') and column_search[1:].isdigit():
                                max_value = int(column_search[1:])
                                item_value = float(column_value) if column_value else 0.0
                                if item_value <= max_value:
                                    filtered_base_data.append(item)
                            elif column_search.endswith('-') and column_search[:-1].isdigit():
                                min_value = int(column_search[:-1])
                                item_value = float(column_value) if column_value else 0.0
                                if item_value >= min_value:
                                    filtered_base_data.append(item)
                            elif column_search.isdigit():
                                target_value = float(column_search.replace(',', ''))
                                item_value = float(column_value) if column_value else 0.0
                                if item_value == target_value:
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
                'batch': item.get('batch'),
                'truck': item.get('truck'),
                'driver': item.get('driver'),
                'startdate': item.get('startdate').strftime('%d-%b-%Y %H:%M'),
                'status': item.get('status'),
                'currentposition': item.get('currentposition'),
                'type': item.get('type'),
                'days': item.get('days'),
                'complete': item.get('complete'),
                'batch_id': item.get('batch_id'),
                'truck_id': item.get('truck_id'),
                'driver_id': item.get('driver_id'),
                'action': ''
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)

    if request.method == 'GET' and trip_id is not None and Trip.objects.filter(id=trip_id, deleted=False).exists():
        for trk in trucks:
            trk_data = {
                'id':trk.id,
                'reg': f"{format_reg(trk.regnumber)}/{format_reg(trk.trailer.regnumber)}" if trk.trailer else f"{format_reg(trk.regnumber)}/-N/A-"
                }
            if trk.trp_truck.exists():
                trip = trk.trp_truck.order_by('-id').first()
                if trip.completed or trip.id == trip_id:
                    trucks_list.append(trk_data)
            else:
                trucks_list.append(trk_data)

        trp = Trip.objects.get(id=trip_id)
        today_date = trp.completeDate if trp.completeDate else datetime.now(pytz.UTC)
        days_taken = (today_date.date() - trp.startDate.date()).days
        if trp.completed:
            days_text = f"{days_taken} days taken to complete trip"
        elif days_taken < 0:
            days_text = f"{abs(days_taken)} days before trip starts"
        else:
            days_text = f"{days_taken} days taken since trip started"

        hist_summary = {'status': 'N/A', 'position': 'N/A', 'dates':'N/A'}
        if Trip_history.objects.filter(trip_id=trip_id).exists():
            hist = Trip_history.objects.filter(trip_id=trip_id).order_by('-id').first()
            hist_summary = {
                'status': hist.tripstatus,
                'position': hist.newposition,
                'dates': hist.statusdate.strftime('%d-%b-%Y')
            }
        trip_data = {
            'id': trp.id,
            'regdate': trp.regdate.strftime('%d-%b-%Y %H:%M:%S'),
            'regby': trp.addedBy.fullname,
            'lastedit': trp.lastEdited.strftime('%d-%b-%Y %H:%M:%S') if trp.lastEdited else "N/A",
            'editor': trp.editedBy.fullname if trp.editedBy else "N/A",
            'loaddate': trp.loadDate.strftime('%d-%b-%Y %H:%M:%S'),
            'loadpoint': trp.loadPoint,
            'weight': trp.cargoWeight,
            'startdate': trp.startDate.strftime('%d-%b-%Y %H:%M:%S'),
            'describe': trp.describe if trp.describe else "N/A",
            'destination': trp.destination,
            'status': hist_summary['status'],
            'currentposition': hist_summary['position'],
            'days': days_text,
            'complete': "Yes" if trp.completed else "No",
            
            'datereg': trp.regdate.strftime('%d-%b-%Y %H:%M'),
            'dateload': trp.loadDate.strftime('%d-%b-%Y'),
            'datestart': trp.startDate.strftime('%d-%b-%Y'),
            'date_load': trp.loadDate,
            'date_start': trp.startDate,

            'batch_id': trp.batch_id,
            'batch': trp.batch.batchnumber,
            'type': trp.batch.batchType,
            'client': trp.batch.client,
            'batch_url': reverse('batch_details', kwargs={'batch_id': trp.batch_id}),
            
            'truck_id': trp.truck_id,
            'truck': f"{format_reg(trp.truck.regnumber)}/{format_reg(trp.truck.trailer.regnumber)}" if trp.truck.trailer else f"{format_reg(trp.truck.regnumber)}/-N/A",
            'truck_url': reverse('truck_details', kwargs={'truck': trp.truck_id}),

            'driver': f"{trp.truck.driver.fullname} - {format_phone(trp.truck.driver.phone)}",
            'driver_url': reverse('driver_details', kwargs={'driver': trp.truck.driver_id}),
        }

        trp_histories = Trip_history.objects.filter(trip_id=trip_id, deleted=False).order_by('id')
        histories = [
            {
                'count': count,
                'regdate': h.regdate.strftime('%d-%b-%Y %H:%M'),
                'staff': h.staff.fullname,
                'status': h.tripstatus,
                'position': h.newposition,
                'status_date': h.statusdate.strftime('%d-%b-%Y')
            }
            for count, h in enumerate(trp_histories, start=1)
        ]

        context = {
            'trip_info': trip_id,
            'trip': trip_data,
            'history': histories,
            'hist': hist_summary,
            'batches': batches_list,
            'trucks': trucks_list
        }
        return render(request, 'trips/trips.html', context)
    
    for trk in trucks:
        trk_data = {
            'id':trk.id,
            'reg': f"{format_reg(trk.regnumber)}/{format_reg(trk.trailer.regnumber)}" if trk.trailer else f"{format_reg(trk.regnumber)}/-N/A-"
            }
        if trk.trp_truck.exists():
            trip = trk.trp_truck.order_by('-id').first()
            if trip.completed:
                trucks_list.append(trk_data)
        else:
            trucks_list.append(trk_data)
    return render(request, 'trips/trips.html', {'batches': batches_list, 'trucks': trucks_list})


@never_cache
def trip_operations(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        delete_trip = request.POST.get('delete_trip')
        complete_id = request.POST.get('complete_id')
        today_date = request.POST.get('today_date')
        
        if complete_id and Trip.objects.filter(id=complete_id).exists():
            trip = Trip.objects.get(id=complete_id)
            if not trip.completed:
                trip.completed = True
                trip.save()

                Trip_history.objects.create(
                    tripstatus = "Complete",
                    staff = request.user,
                    newposition = trip.destination,
                    statusdate = today_date,
                    trip = trip,
                )
            fdback = {"success": True, "sms": "Trip's been marked as complete.."}
            
        elif trip_id is not None and delete_trip is not None:
            try:
                trp = Trip.objects.get(id=trip_id)
                trp.deleted = not trp.deleted
                trp.save()
                fdback = {'success': True, 'sms': 'Success'}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        elif trip_id is not None and delete_trip is None:
            try:
                trip_instance = Trip.objects.get(id=int(trip_id))
                form = TripForm(request.POST, instance=trip_instance)
                if form.is_valid():
                    trp = form.save(commit=False)
                    trip_truck = Truck.objects.get(id=int(request.POST.get('truck')))
                    trp.trailer = trip_truck.trailer
                    trp.driver = trip_truck.driver
                    trp.editedBy = request.user
                    trp.lastEdited = datetime.now().replace(tzinfo=pytz.UTC)
                    trp.describe = form.cleaned_data.get('describe') or None
                    trp.save()
                    fdback = {'success': True, 'sms': 'Information updated successfully!'}
                else:
                    errorMsg = "Unknown error."
                    if 'destination' in form.errors:
                        errorMsg = form.errors['destination'][0]
                    if 'loadPoint' in form.errors:
                        errorMsg = form.errors['loadPoint'][0]
                    fdback = {'success': False, 'sms': errorMsg}
            except Exception as e:
                print(e)
                fdback = {'success': False, 'sms': 'Operation failed!'}

        else:
            try:
                trip_trucks_list = request.POST.get('trucks').split(',')
                form_success = True
                form_sms = 'New trip added to this batch successfully!'
                
                for truck_id in trip_trucks_list:
                    form_data = request.POST.copy()
                    trip_truck = Truck.objects.get(id=int(truck_id))
                    form_data['truck'] = trip_truck
                    form_data['trailer'] = trip_truck.trailer
                    form_data['driver'] = trip_truck.driver
                    form_data['cargoWeight'] = float(request.POST.get('cargoWeight'))/float(len(trip_trucks_list))
                    form = TripForm(form_data)
                    if form.is_valid():
                        trip = form.save(commit=False)
                        trip.addedBy = request.user
                        trip.save()
                    else:
                        print(form.errors)
                        form_success = False
                        form_sms = 'Operation failed.'
                        break

                fdback = {'success': form_success, 'sms': form_sms}
            except Exception as e:
                fdback = {'success': False, 'sms': f'Operation failed: {str(e)}'}

        return JsonResponse(fdback)
    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})


@never_cache
def add_trip_history(request):
    if request.method == 'POST':
        try:
            form = Trip_historyForm(request.POST)
            if form.is_valid():
                hist = form.save(commit=False)
                hist.staff = request.user
                hist.save()
                fdback = {'success': True, 'sms': 'Trip history updated successfully!', 'dates': hist.regdate.strftime('%d-%b-%Y %H:%M'), 'staff':hist.staff.fullname, 'status':hist.tripstatus, 'pos': hist.newposition, 'st_date': hist.statusdate.strftime('%d-%b-%Y')}
            else:
                errorMsg = "Unknown error."
                if 'newposition' in form.errors:
                    errorMsg = form.errors['newposition'][0]
                if 'tripstatus' in form.errors:
                    errorMsg = form.errors['tripstatus'][0]
                fdback = {'success': False, 'sms': errorMsg}
        except Exception as e:
            print(e)
            fdback = {'success': False, 'sms': 'Operation failed!'}
        return JsonResponse(fdback)
    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})


@never_cache
def batches_page(request, batch_id=None):
    if request.method == 'POST' and batch_id is None:
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Batch.objects.exclude(deleted=True)

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
        for btc in queryset:
            trucks_count = Trip.objects.filter(batch=btc).count()
            comp_count = "No" if Trip.objects.filter(batch=btc, completed=False).count() > 0 else "Yes"
            batch_data = {
                'id': btc.id,
                'regdate': btc.regdate,
                'batchnumber': btc.batchnumber,
                'type': btc.batchType,
                'client': btc.client,
                'trucks': trucks_count,
                'complete': comp_count if Trip.objects.filter(batch=btc).exists() else "N/A"
            }
            base_data.append(batch_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'id',
            1: 'regdate',
            2: 'batchnumber',
            3: 'type',
            4: 'client',
            5: 'trucks',
            6: 'complete'
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'batchnumber')
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
                        if column_field in ('type', 'complete'):
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
                'batchnumber': item.get('batchnumber'),
                'type': item.get('type'),
                'client': item.get('client'),
                'trucks': item.get('trucks'),
                'complete': item.get('complete'),
                'action': ''
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)
    
    if request.method == 'GET' and batch_id is not None and Batch.objects.filter(id=batch_id, deleted=False).exists():
        btc = Batch.objects.get(id=batch_id)
        batch_trips = Trip.objects.filter(batch=btc)
        comp_count = "No" if Trip.objects.filter(batch=btc, completed=False).count() > 0 else "Yes"

        get_trucks = Truck.objects.filter(deleted=False)
        available_trucks_list = []
        for trk in get_trucks:
            trk_data = {
                'id':trk.id,
                'reg': f"{format_reg(trk.regnumber)}/{format_reg(trk.trailer.regnumber)}" if trk.trailer else f"{format_reg(trk.regnumber)}/-N/A-"
                }
            if trk.trp_truck.exists():
                trip = trk.trp_truck.order_by('-id').first()
                if trip.completed:
                    available_trucks_list.append(trk_data)
            else:
                available_trucks_list.append(trk_data)
        
        trips_list = []
        for count, trip in enumerate(batch_trips, start=1):
            status = "N/A"
            position = "N/A"
            
            if Trip_history.objects.filter(trip=trip).exists():
                hist = Trip_history.objects.filter(trip=trip).order_by('-id').first()
                status = hist.tripstatus
                position = hist.newposition

            trips_list.append({
                'count': count,
                'loaddate': trip.loadDate.strftime('%d-%b-%Y %H:%M'),
                'startdate': trip.startDate.strftime('%d-%b-%Y %H:%M'),
                'driver': trip.truck.driver.fullname,
                'status': status,
                'position': position,
                'complete': "Yes" if trip.completed else "No",
                'url': reverse('trip_details', kwargs={'trip_id': trip.id})
            })

        batch_data = {
            'id': batch_id,
            'regdate': btc.regdate.strftime('%d-%b-%Y %H:%M:%S'),
            'regby': btc.addedBy.fullname,
            'batchNo': btc.batchnumber,
            'type': btc.batchType,
            'client': btc.client,
            'trucks': batch_trips.count(),
            'complete': comp_count if Trip.objects.filter(batch=btc).exists() else "N/A",
            'info': btc.describe if btc.describe else '-',
            'lastEdit': btc.lastEdited.strftime('%d-%b-%Y %H:%M:%S') if btc.lastEdited else "N/A",
            'editby': btc.editedBy.fullname if btc.editedBy else "N/A",
        }

        context = {
            'batch_info': batch_id,
            'batch': batch_data,
            'batch_trips': trips_list,
            'trucks_list': available_trucks_list
        }

        return render(request, 'trips/batches.html', context)
    return render(request, 'trips/batches.html')


@never_cache
def batch_operations(request):
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        delete_batch = request.POST.get('delete_batch')

        if batch_id is not None and delete_batch is not None:
            try:
                btc = Batch.objects.get(id=batch_id)
                btc.deleted = not btc.deleted
                btc.save()
                fdback = {'success': True, 'sms': 'Success'}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        elif batch_id is not None and delete_batch is None:
            try:
                batch_instance = Batch.objects.get(id=batch_id)
                form = BatchForm(request.POST, instance=batch_instance)
                if form.is_valid():
                    trl = form.save(commit=False)
                    trl.editedBy = request.user
                    trl.lastEdited = datetime.now().replace(tzinfo=pytz.UTC)
                    trl.describe = form.cleaned_data.get('describe') or None
                    trl.save()
                    fdback = {'success': True, 'sms': 'Information updated successfully!'}
                else:
                    errorMsg = "Unknown error."
                    if 'batchnumber' in form.errors:
                        errorMsg = form.errors['batchnumber'][0]
                    fdback = {'success': False, 'sms': errorMsg}
            except Exception as e:
                print(e)
                fdback = {'success': False, 'sms': 'Operation failed!'}

        else:
            try:
                form = BatchForm(request.POST)
                if form.is_valid():
                    btc = form.save(commit=False)
                    btc.addedBy = request.user
                    btc.save()
                    fdback = {'success': True, 'sms': 'New batch added successfully!', 'id':btc.id, 'batch': btc.batchnumber, 'type':btc.batchType, 'client':btc.client}
                else:
                    errorMsg = "Unknown error."
                    if 'batchnumber' in form.errors:
                        errorMsg = form.errors['batchnumber'][0]
                    fdback = {'success': False, 'sms': errorMsg}
            except Exception as e:
                fdback = {'success': False, 'sms': 'Operation failed!'}
        
        return JsonResponse(fdback)
    return JsonResponse({'success': False, 'sms': 'Invalid form data!'})


@never_cache
def op_report_page(request):
    if request.method == 'POST':
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Base queryset
        queryset = Trip.objects.exclude(deleted=True)

        # Date range filtering
        load_startdate = request.POST.get('load_startdate')
        load_enddate = request.POST.get('load_enddate')
        trip_startdate = request.POST.get('trip_startdate')
        trip_enddate = request.POST.get('trip_enddate')
        date_range_filters = Q()
        if load_startdate:
            load_startdate = datetime.strptime(load_startdate, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(loadDate__gte=load_startdate)
        if load_enddate:
            load_enddate = datetime.strptime(load_enddate, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(loadDate__lte=load_enddate)
        
        if trip_startdate:
            trip_startdate = datetime.strptime(trip_startdate, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(startDate__gte=trip_startdate)
        if trip_enddate:
            trip_enddate = datetime.strptime(trip_enddate, format_datetime).astimezone(tz_tzone)
            date_range_filters |= Q(startDate__lte=trip_enddate)

        if date_range_filters:
            queryset = queryset.filter(date_range_filters)


        # Base data from queryset
        base_data = []
        for trp in queryset:
            days_loading = (datetime.now(pytz.UTC).date() - trp.loadDate.date()).days
            days_started = (datetime.now(pytz.UTC).date() - trp.startDate.date()).days

            trip_status = "N/A"
            trip_position = "N/A"
            if Trip_history.objects.filter(trip_id=trp.id, deleted=False).exists():
                history = Trip_history.objects.filter(trip_id=trp.id, deleted=False).order_by('-id').first()
                trip_status = history.tripstatus
                trip_position = history.newposition

            trip_data = {
                'batch': trp.batch.batchnumber,
                'type': trp.batch.batchType,
                'client': trp.batch.client,
                'truck': f"{format_reg(trp.truck.regnumber)}/{format_reg(trp.truck.trailer.regnumber)}" if trp.truck.trailer else f"{format_reg(trp.truck.regnumber)}/-N/A",
                'driver': trp.truck.driver.fullname,
                'currentposition': trip_position,
                'status': trip_status,
                'loaddate': trp.loadDate,
                'startdate': trp.startDate,
                'days_loading': 0 if days_loading < 0 else days_loading,
                'complete': "Yes" if trp.completed else "No",
                'days_start': 0 if days_started < 0 else days_started,
            }
            base_data.append(trip_data)

        
        # Total records before filtering
        total_records = len(base_data)

        # Define a mapping from DataTables column index to the corresponding model field
        column_mapping = {
            0: 'batch',
            1: 'batch',
            2: 'type',
            3: 'client',
            4: 'truck',
            5: 'driver',
            6: 'currentposition',
            7: 'status',
            8: 'loaddate',
            9: 'startdate',
            10: 'days_loading',
            11: 'days_start',
            12: 'complete',
        }

        # Apply sorting
        order_column_name = column_mapping.get(order_column_index, 'startdate')
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
                        if column_field in ('type', 'complete'):
                            if column_search.lower() == column_value:
                                filtered_base_data.append(item)
                        elif column_field in ('days_loading', 'days_start'):
                            if column_search.startswith('-') and column_search[1:].isdigit():
                                max_value = int(column_search[1:])
                                item_value = float(column_value) if column_value else 0.0
                                if item_value <= max_value:
                                    filtered_base_data.append(item)
                            elif column_search.endswith('-') and column_search[:-1].isdigit():
                                min_value = int(column_search[:-1])
                                item_value = float(column_value) if column_value else 0.0
                                if item_value >= min_value:
                                    filtered_base_data.append(item)
                            elif column_search.isdigit():
                                target_value = float(column_search.replace(',', ''))
                                item_value = float(column_value) if column_value else 0.0
                                if item_value == target_value:
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
                'batch': item.get('batch'),
                'type': item.get('type'),
                'client': item.get('client'),
                'truck': item.get('truck'),
                'driver': item.get('driver'),
                'currentposition': item.get('currentposition'),
                'status': item.get('status'),
                'loaddate': item.get('loaddate').strftime('%d-%b-%Y %H:%M'),
                'startdate': item.get('startdate').strftime('%d-%b-%Y %H:%M'),
                'todaydate': (datetime.now(pytz.UTC).date()).strftime('%d-%b-%Y'),
                'daysLoading': item.get('days_loading'),
                'complete': item.get('complete'),
                'daysGoing': item.get('days_start'),
                'goReturn': "N/A",
            })

        ajax_response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': final_data,
        }
        return JsonResponse(ajax_response)
    return render(request, 'trips/report.html')