from django.shortcuts import render, get_object_or_404
from .models import Event, EventTicket, UserProfile
from django.views.generic import ListView, DetailView
from django.db.models import Max, Min
from order.models import Order, OrderItem
import json
from django.http import JsonResponse

def home(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'afriventapp/home.html', context)


# class EventDetailView(DetailView):
#     model = Event
#     template_name = "afriventapp/event-dashboard.html"
#     context_object_name = 'event'


#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['tickets'] = EventTicket.objects.filter()
#         return context
    
    
def EventDetailView(request, slug):
    event =  get_object_or_404(Event, slug=slug)
    ticket = EventTicket.objects.filter(event=event)
    ticket_price_range = ticket.aggregate(min_price=Min('amount'), max_price=Max('amount'))
    context = {
        'event':event,
        'tickets':ticket,
        'ticket_price_range': ticket_price_range
    }
    return render(request, 'afriventapp/event-dashboard.html', context)


def userdashboard(request, pk):
    # user = get_object_or_404(user)
    user_profile = get_object_or_404(UserProfile, user=pk)
    events = Event.objects.filter(creator = user_profile)
    orders = Order.objects.filter( user = pk)
    tickets = OrderItem.objects.filter(user = pk)
    print(user_profile.user.first_name)
    context = {
        'user_profile':user_profile,
        'events':events,
        'orders':orders,
        'tickets': tickets
    }
    return render(request, 'afriventapp/user-dashboard.html', context)


def event_order_details(request, eventId):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    events = Event.objects.filter(creator = user_profile)
    if request.method == "GET":
        orderDetails = Order.objects.filter(event_id=eventId).exclude(payment_confirmation = False).values()
        # totalOrderPrice  = Order.objects.filter(event_id=eventId).values('total_cost')
    context = {
        'user_profile':user_profile,
        'orderDetails':orderDetails,

    }
    return JsonResponse(
        {'orderDetails':list(orderDetails)}
        # {'totalOrderPrice': sum(list(totalOrderPrice))}
        )