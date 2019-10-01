from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from afriventapp.models import UserProfile

class Register(UserCreationForm):
    first_name= forms.CharField(max_length = 50)
    last_name= forms.CharField(max_length = 50)
    email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address')
    address = forms.CharField(max_length = 100)
    phone_number = PhoneNumberField(help_text='Enter your phone number with country code (i.e +23490xxxxxxx)')


    class meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email',   'password1',
                     'password2', 'address', 'phone_number')

class UserProfileForm(forms.ModelForm):
    class meta:
        model = UserProfile
        fields = ['address', 'phone_number', 'bio']



# class Register(forms.Form):
#     first_name= forms.CharField(label="first_name", max_length = 50)
#     last_name= forms.CharField(label="last_name", max_length = 50)
#     email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address')

