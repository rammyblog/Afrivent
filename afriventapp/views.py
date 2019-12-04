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
from django.core.paginator import Paginator
# from afriventapp.models import Event
from django.contrib.auth.models import User
from datetime import date
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from order.generate_barcode import barcodeGenerator
import base64
from django.core.files.base import ContentFile


def home(request):
    events = Event.objects.all()[:9]
    top_events = Event.objects.all()[:2]
    context = {
        'events': events,
        'top_events': top_events
        }
    return render(request, 'afriventapp/event_app/home.html', context)


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


def all_events(request):
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'afriventapp/event_app/events.html', {'events': events})

    
    
def EventDetailView(request, slug):
    event =  get_object_or_404(Event, slug=slug)
    ticket = EventTicket.objects.filter(event=event)
    ticket_price_range = ticket.aggregate(min_price=Min('amount'), max_price=Max('amount'))
    events = Event.objects.all()[:9]
    context = {
        'event':event,
        'events':events,
        'tickets':ticket,
        'ticket_price_range': ticket_price_range
    }
    return render(request, 'afriventapp/event_app/single.html', context)

@login_required
def userdashboard(request, pk):
    # user = get_object_or_404(user)
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=pk)
    events = Event.objects.filter(creator = user_profile)
    orders = Order.objects.filter( user = user)
    # registeredOrders = Order.objects.filter(user =)
    tickets = OrderItem.objects.filter(user = user)
    print(request.user.username, user)
    context = {
        'user_profile':user_profile,
        'events':events,
        'orders':orders,
        'tickets': tickets,
        'user':user

    }
    return render(request, 'afriventapp/user-dashboard.html', context)

@login_required
def generateTicket(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    reference_code = order.ref_code
    if order.payment_confirmation == True:
        barcode = barcodeGenerator(order.id, order.event, reference_code, order.order_unique_id, order.user)
        # format, imgstr = barcode.split(';base64,') 
        # print(barcode)
        # ext = format.split('/')[-1] 
        # barcode = ContentFile(base64.b64decode(imgstr), name='{}.'.format(order.id) + ext)


    else:
        return render(request, 'afriventapp/404.html', context={
            'order':order
        })
 
    context = {
        'order': order,
        'order_items' : order_items,
        'barcode':barcode
    }

    return render(request, 'order/ticket.html', context) 


def requestPayout(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=pk)
    #send_mail()`
    user_profile.balance -= user_profile.balance
    user_profile.save()
    context = {}
    return render(request, 'afriventapp/requestPayout.html', context)
    



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

@login_required
def createEventForm(request):
    return render(request, 'afriventapp/create-event.html')


@login_required
def eventCreated(request):
    if request.method == 'POST':
        queryDict = request.POST
        
        ticketType = queryDict.getlist('type')
        ticketAmount = queryDict.getlist('amount')
        ticketQuantity = queryDict.getlist('quantity')
        print(queryDict)
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

@login_required
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


def search(request):
    try:
        if request.method == 'GET':
            query = request.GET['q']
            events = Event.objects.filter(Q(event_name__icontains = request.GET['q']) |
            Q(creator__user__username__icontains= request.GET['q']) | Q(description__icontains = request.GET['q']) )
        context = {'events':events, 'query':query}
        if events:
            
            print(events)            
            return render(request, 'afriventapp/search.html', context)
        else:
            return render(request, 'afriventapp/search.html')
    except MultiValueDictKeyError as e:
        print(e)
        return render(request, 'afriventapp/404.html')
