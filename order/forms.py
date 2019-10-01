from django import forms

class OrderForm(forms.Form):
    order_type = forms.CharField(max_length=200)
    order_quantity = forms.IntegerField()
    order_unit_price = forms.IntegerField()