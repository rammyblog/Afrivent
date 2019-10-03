from django import forms
from afriventapp.models import Event, EventTicket

# class CreateEven

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields =  ('event_name', 'address', 'event_image', 'description', 
                'start_date', 'start_time' , 'end_date', 'end_time')

class TicketForm(forms.ModelForm):
    class Meta:
        model = EventTicket
        fields = ('type','quantity', 'amount')