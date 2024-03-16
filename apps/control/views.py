from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


@never_cache
def users_page(request, user_id=None):
    context = {
        'user_info': user_id
    }
    return render(request, 'control/users.html', context)

@never_cache
def logs_page(request, user_id=None):
    context = {
        'user_logs': user_id
    }
    return render(request, 'control/logs.html', context)