from django.contrib import admin
from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'ticket', 'quantity')
    list_filter = ('order','ticket')


# admin.site.register(UserProfile)