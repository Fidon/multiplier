from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from apps.control.forms import CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@never_cache
def login_page(request):
    if request.user.is_authenticated:
        response = redirect("/home")
        response.set_cookie('user_id', request.user.username)
        response.set_cookie('dept_id', request.user.department_id)
        return response
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.blocked:
                login(request, user)
                response = JsonResponse({'success': True, 'sms': 'success'})
                response.set_cookie('user_id', user.username)
                response.set_cookie('dept_id', user.department_id)
        else:
            response = JsonResponse({'success': False, 'sms': form.errors['__all__'][0], 'error':form.errors})
        return response
    return render(request, 'auth.html')


@never_cache
def home_page(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': '200'})
    return JsonResponse({'message': '405'})