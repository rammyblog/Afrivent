from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('process', views.orderProcess, name="orderProcess"),
    path('process/confirm', views.orderConfimation, name="orderConfirmation"),
    path('payment/process', views.processPayment, name='process'),
    path('payment/confirm', views.confirmPayment, name='confirm-payment'),
    # path('ticketpage/', views.ticketPage, name='ticket-page')
]