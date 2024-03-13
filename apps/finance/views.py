from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required


@never_cache
def expenses_page(request, exp=None):
    context = {
        'exp_info': exp
    }
    return render(request, 'finance/expenses.html', context)

@never_cache
def income_page(request, income=None):
    context = {
        'income_info': income
    }
    return render(request, 'finance/income.html', context)

@never_cache
def reports_page(request):
    return render(request, 'finance/report.html')