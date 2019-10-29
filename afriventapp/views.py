from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, redirect
from .models import Event, EventTicket, UserProfile
from django.views.generic import ListView, DetailView
from django.db.models import Max, Min
from order.models import Order, OrderItem
import json
from django.http import JsonResponse
from django.http import HttpResponse
from afriventapp.forms import EventForm, TicketForm
from django.views.generic.edit import UpdateView
# from afriventapp.models import Event


def home(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'afriventapp/home.html', context)


# class EventDetailView(DetailView):
#     model = Event
#     template_name = "afriventapp/event-dashboard.html"
#     context_object_name = 'event'


#     def get_context_data(self, **kwargs):    from django.views.generic.edit import UpdateView


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


def createEventForm(request):
    return render(request, 'afriventapp/create-event.html')

def eventCreated(request):
    if request.method == 'POST':
        queryDict = request.POST
        ticketType = queryDict.getlist('type')
        ticketAmount = queryDict.getlist('amount')
        ticketQuantity = queryDict.getlist('quantity')
        # print(list(dataDict))
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            user_profile = get_object_or_404(UserProfile, user=request.user)
            event.creator =  user_profile
            print('hi')
            event.save()
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket_event = get_object_or_404(Event, pk=event.id)
                for ticket in range(len(ticketType)):
                    EventTicket.objects.create(
                        type = ticketType[ticket],
                        quantity = ticketQuantity[ticket],
                        amount = ticketAmount[ticket],
                        event = ticket_event
                    )
            return HttpResponse(reverse('afrivent:event-detail', args=(event.slug,)))
            
    else:
        form = EventForm()
    
    return redirect('afrivent:event-detail', event.slug)



class EventUpdate(UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'afriventapp/edit-event.html'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['ticket'] = EventTicket.objects.filter(event=self.object) 
            context_object_name = 'EventTicket'
            print(context_object_name)
        #     if context_object_name:
        #         context[context_object_name] = self.object
        # context.update(kwargs)
        return super().get_context_data(**context)


def eventUpdate(request, event_slug):
    event_edit =  get_object_or_404(Event, slug=event_slug)
    ticketquery = EventTicket.objects.filter(event=event_edit)
    if request.method == 'POST':
        queryDict = request.POST
        ticketType = queryDict.getlist('type')
        ticketAmount = queryDict.getlist('amount')
        ticketQuantity = queryDict.getlist('quantity')
        event_form = EventForm(request.POST, request.FILES, instance = event_edit)
        if event_form.is_valid():
            event_form.save()
            ticketform = TicketForm(request.POST) 
            ticketquery.delete()
            for ticket in range(len(ticketType)):
                EventTicket.objects.create(
                        type = ticketType[ticket],
                        quantity = ticketQuantity[ticket],
                        amount = ticketAmount[ticket],
                        event = event_edit
                    )

            return redirect(reverse('afrivent:event-detail', args=(event_slug,)))
            
    else:
        event_form = EventForm()
        ticketform = TicketForm()

    context = {

        'event': event_edit,
        'ticket': ticketquery
    }
    return render(request, 'afriventapp/edit-event.html', context)

