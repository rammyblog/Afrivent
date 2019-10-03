from django.db import models
from django.contrib.auth.models import User
from afriventapp.models import EventTicket, Event
import uuid

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='event_ordered', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    authorization_url = models.URLField(blank=True)
    ref_code = models.CharField(max_length=250)
    payment_confirmation = models.BooleanField(default=False)
    access_code = models.CharField(max_length=1000, null=True)
    order_unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.event)



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, related_name='order_ticket',on_delete=models.CASCADE)
    ticket = models.ForeignKey(EventTicket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.ticket)
