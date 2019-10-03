from django.urls import path
from . import views

app_name = 'afrivent'

urlpatterns = [
    path('', views.home, name="home"),
    path('event-order/details/<int:eventId>', views.event_order_details, name='event-order-details'),
    path('event/<slug>', views.EventDetailView, name='event-detail'),
    path('profile/<pk>', views.userdashboard, name='user-profile'),
    path('create/event', views.createEventForm, name='create-event'),
    path('new/event/created', views.eventCreated, name='event-created'),

   
]