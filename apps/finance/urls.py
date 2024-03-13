from django.urls import path
from . import views as v

urlpatterns = [
    path('expenses/', v.expenses_page, name='expenses'),
    path('expenses/<int:exp>/', v.expenses_page, name='exp_details'),
    path('income/', v.income_page, name='income'),
    path('income/<int:income>/', v.income_page, name='income_details'),
    path('reports/', v.reports_page, name='fin_report'),
]
