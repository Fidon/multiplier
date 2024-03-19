from django.urls import path
from . import views as v

urlpatterns = [
    path('users/', v.users_page, name='users'),
    path('users/<int:user_id>/', v.users_page, name='user_details'),
    path('users/newuser/', v.users_operations, name='users_operations'),
    path('system-logs/', v.logs_page, name='logs'),
    path('system-logs/<int:user_id>/', v.logs_page, name='userlogs'),
]
