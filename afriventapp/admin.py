from django.contrib import admin
from .models import Event, EventTicket, UserProfile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    # prepopulated_fields = ('slug')


@admin.register(EventTicket)
class EventTicketAdmin(admin.ModelAdmin):
    list_display = ('type', 'event', 'amount')
    list_filter = ('type','amount')


admin.site.register(UserProfile)