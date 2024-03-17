from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .models import Department, CustomUser
from .forms import CustomUserForm, CustomAuthenticationForm
# from django.contrib.auth.decorators import login_required


@never_cache
def users_page(request, user_id=None):
    if request.method == 'POST':
        pass
    departments = Department.objects.filter(deleted=False)
    context = {
        'user_info': user_id,
        'departments': departments,
    }
    return render(request, 'control/users.html', context)

@never_cache
def users_actions(request):
    if request.method == 'POST':
        try:
            form = CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                fdback = {'success': True, 'sms': 'User added successfully!'}
            else:
                errorMsg = ""
                if 'username' in form.errors:
                    errorMsg = form.errors['username'][0]
                if 'department' in form.errors:
                    errorMsg = form.errors['department'][0]
                if 'full_name' in form.errors:
                    errorMsg = form.errors['full_name'][0]
                if 'phone' in form.errors:
                    errorMsg = form.errors['phone'][0]
                fdback = {'success': False, 'sms': errorMsg}
        except Exception as e:
            fdback = {'success': False, 'sms': 'Unknown error!'}
    return JsonResponse(fdback)


@never_cache
def logs_page(request, user_id=None):
    context = {
        'user_logs': user_id
    }
    return render(request, 'control/logs.html', context)