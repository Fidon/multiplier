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
def revenue_page(request, rev=None):
    context = {
        'rev_info': rev
    }
    return render(request, 'finance/revenue.html', context)

@never_cache
def reports_page(request):
    return render(request, 'finance/reports.html')