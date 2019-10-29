from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.shortcuts import render,redirect, get_object_or_404
from celery.decorators import task
from afriventapp.models import Event, EventTicket,UserProfile
from order.models import Order, OrderItem

@task
def reconcileOrder(order_id):
    # order_id = request.session['order_id']
    order = get_object_or_404(Order, pk=order_id)
    event = get_object_or_404(Event, id= order.event.id)
    OrderItems = OrderItem.objects.filter(order=order)
    for orderItem in OrderItems:
        ticketType = get_object_or_404(EventTicket, pk=orderItem.ticket.id)
        quantity = orderItem.quantity # Get the quantity the user initizlly ordered
        ticketType.quantity += quantity
        ticketType.save()
    order.delete()
    return True

@task(name="sum_two_numbers")
def add(x, y):
    return x + y