from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from apps.dbase.models import Selcompay, Lipanamba, Debts, Loans
# from datetime import datetime, timedelta
# from dateutil import relativedelta
# from django.db.models import F, Sum
# import pytz


@never_cache
def login_page(request):
    if request.method == 'POST':
        return render(request, 'home.html')
    return render(request, 'auth.html')


@never_cache
def home_page(request):
    return render(request, 'home.html')