from django.urls import path
from . import views as v

urlpatterns = [
    path('expenses/', v.expenses_page, name='expenses'),
    path('expenses/<int:exp>/', v.expenses_page, name='exp_details'),
    path('revenue/', v.revenue_page, name='revenue'),
    path('revenue/<int:revenue>/', v.revenue_page, name='revenue_details'),
    path('invoices/', v.invoices_page, name='invoices'),
    path('invoices/<int:invoice>/', v.invoices_page, name='invoice_details'),
    path('reports/', v.reports_page, name='fin_report'),
]
