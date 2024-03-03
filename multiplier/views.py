from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout


@never_cache
def login_page(request):
    if request.method == 'POST':
        return render(request, 'home.html')
    return render(request, 'auth.html')


@never_cache
def home_page(request):
    return render(request, 'home.html')