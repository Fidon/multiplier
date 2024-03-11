from django.urls import path
from . import views as v

urlpatterns = [
    path('expenses/', v.expenses_page, name='expenses'),
    path('expenses/<int:exp>/', v.expenses_page, name='exp_details'),
    path('revenue/', v.revenue_page, name='revenue'),
    path('revenue/<int:rev>/', v.revenue_page, name='revenue'),
    path('reports/', v.reports_page, name='fin_report'),
]