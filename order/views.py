from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from order.forms import OrderForm
import json
from afriventapp.models import Event, EventTicket,UserProfile
from order.models import Order, OrderItem
from django.http import JsonResponse
from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from python_paystack.paystack_config import PaystackConfig
# from paystack import verify




def orderProcess(request):
    if request.method == 'POST':
        queryDict = request.POST
        dataDict = queryDict.dict()
        eventID = dataDict['event']
        tickets =json.loads(dataDict['ticket'])
        price = json.loads(dataDict['price'])
        total = dataDict['total'];
        event = get_object_or_404(Event, pk=eventID)
        order = Order.objects.create(
            user = request.user,
            event = get_object_or_404(Event, pk=eventID),
            total_cost = total
            )
        for ticket in tickets.keys():
            ticketType = get_object_or_404(EventTicket, pk=ticket)
            quantity = tickets[ticket] # Get the quantity the user wants
            OrderItem.objects.create(
                user = request.user,
                order = order,
                ticket = ticketType,
                quantity = quantity
            )
            ticketType.quantity -= quantity
            ticketType.save()
        request.session['order_id']=order.id
        # return redirect(reverse('order:process'))
    # transaction = Transaction(2000, 'email@test.com')
    # transaction_manager = TransactionsManager()
    # transaction = transaction_manager.initialize_transaction('STANDARD', transaction)        

    
    return render(request, 'order/index.html')



def processPayment(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, pk=order_id)
    PaystackConfig.SECRET_KEY  = 'sk_test_4bc9c2030fe11485c51ce1692428ce37663c9d6c'
    PaystackConfig.PUBLIC_KEY = 'pk_test_66242613f73c8034560a3eecf9d248787f776bdb'
    transaction = Transaction(100000, 'onasanyatunde67@gmail.com')
    transaction_manager = TransactionsManager() 
    transaction = transaction_manager.initialize_transaction('STANDARD', transaction)
    # request.session['transaction'] = transaction  
    order.authorization_url = transaction.__dict__['authorization_url']
    order.ref_code = transaction.__dict__['reference']
    order.access_code = transaction.__dict__['access_code']
    order.payment_confirmation = False
    order.save()
    # send email here
    print(transaction.__dict__)
    return redirect(transaction.__dict__['authorization_url'])


def confirmPayment(request):
    order_id = request.session['order_id']
#   transaction = request.session['transaction']
#   print(transaction )
    order = get_object_or_404(Order, pk=order_id)

    ref_code = order.ref_code
    transaction_manager = TransactionsManager() 
    transaction_verify = transaction_manager.verify_transaction(ref_code)
    if transaction_verify == "success":
        order.payment_confirmation = True
        user = get_object_or_404(UserProfile, pk=order.event.creator.id)
        user.balance += order.total_cost
        user.save()
        order.save()
    else:
        order.payment_confirmation = False
        #Send Email
        order.save()
#   transaction_verify = 'https://api.paystack.co/transaction/verify/{0}'.format(ref_code)

    return render(request, 'order/success.html') 



