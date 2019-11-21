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
from order.confirm_paystack_payment import confirmPaystackPayment
from order.tasks import reconcileOrder
# from paystack import verify
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from celery import app
from celery import current_app
from celery.task.control import revoke
from celery.result import AsyncResult
from order.generate_barcode import barcodeGenerator
import base64
from django.core.files.base import ContentFile



@never_cache
# @csrf_exempt  
@login_required 
def orderConfimation(request):
    print(request.method)
    order_id = request.session['order_id']
    order = get_object_or_404(Order, pk=order_id)
    event = get_object_or_404(Event, id= order.event.id)

    if request.session['order_exist']:
        result = reconcileOrder.apply_async((order_id,), countdown=600)
        request.session['task_id'] = result.id
        OrderItems = OrderItem.objects.filter(order=order)
        request.session['order_exist'] = False
    else:
        return render(request, 'order/failedOrder.html', context={
            'order':order
        })


    # print('hi', request.META['HTTP_REFERER'])    


    # else:
    #     return redirect(reverse('afrivent:home'))


    context = {
    'order' : order,
    'event' : event,
    }

    return render(request, 'order/confirm.html', context)


@login_required
def orderProcess(request):
    if request.method == 'POST':
        queryDict = request.POST
        print(queryDict)
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
            # ticketType.quantity -= quantity
            ticketType.save()
        
        request.session['order_id'] = order.id
        request.session['order_exist'] = True

        # return redirect('order:orderConfirmation')
        


        
        # result = reconcileOrder.apply_async((order.id,), countdown=120)
        # request.session['task_id'] = result.id
        


    else:
        print('hiiiiiiiiiiiiiiiiii')
    
        # return redirect(reverse('order:process'))
    # transaction = Transaction(2000, 'email@test.com')
    # transaction_manager = TransactionsManager()
    # transaction = transaction_manager.initialize_transaction('STANDARD', transaction)        
    context = {'order':order}

    
    return render(request, 'order/confirm.html', context)


@never_cache
@login_required
def processPayment(request):
    
    order_id = request.session['order_id']
    task_id = request.session['task_id']
    current_app.control.revoke(task_id)
    order = get_object_or_404(Order, pk=order_id)
    print(reconcileOrder.AsyncResult(task_id).state)

    # if reconcileOrder.AsyncResult(task_id).state == 'REVOKED':
    #     return render(request, 'order/failed.html', context={
    #         'order': order
    #     } )
    # else:
    PaystackConfig.SECRET_KEY  = 'sk_test_4bc9c2030fe11485c51ce1692428ce37663c9d6c';
    PaystackConfig.PUBLIC_KEY = 'pk_test_66242613f73c8034560a3eecf9d248787f776bdb';
    orderAmountKobo = order.total_cost *  100
    transaction = Transaction(orderAmountKobo, order.user.email)
    transaction_manager = TransactionsManager() 
    transaction = transaction_manager.initialize_transaction('STANDARD', transaction)
    # request.session['transaction'] = transaction  
    order.authorization_url = transaction.__dict__['authorization_url']
    order.ref_code = transaction.__dict__['reference']
    order.access_code = transaction.__dict__['access_code']
    order.payment_confirmation = False
    order.save()
    # request.session['order_exist'] = True
    # send email here
# print(transaction.__dict__)
    return redirect(transaction.__dict__['authorization_url'])

@login_required
def confirmPayment(request):
    reference_code = request.GET.dict()['reference']
    order = get_object_or_404(Order, ref_code=reference_code)
    order_items = OrderItem.objects.filter(order=order)

    if confirmPaystackPayment(reference_code) == 'success':
        order.payment_confirmation = True
        user = get_object_or_404(UserProfile, pk=order.event.creator.id)
        barcode = barcodeGenerator(order.id, order.event, reference_code, order.order_unique_id, user)
        format, imgstr = barcode.split(';base64,') 
        ext = format.split('/')[-1] 
        barcode = ContentFile(base64.b64decode(imgstr), name='{}.'.format(order.id) + ext)
        user.balance += order.total_cost
        order.order_barcode = barcode
        user.save()
        order.save()
            # ticketType.quantity -= quantity
        for order_item in order_items:
            ticketType = get_object_or_404(EventTicket, pk=order_item.ticket.pk)
            ticketType.quantity -= order_item.quantity
            ticketType.save()


    else:
        order.payment_confirmation = False
        # reconcileOrder.delay(order.id)
        # request.session['task_id'] = result.id
        #Send Email
        order.save()
        return render(request, 'order/failedPayment.html', context={
            'order':order
        })
 
    context = {
        'order': order,
        'order_items' : order_items
    }

    return render(request, 'order/success.html', context) 




# def confirmPaymentID(request, pk):
