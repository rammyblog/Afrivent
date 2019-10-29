from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from afriventapp.models import UserProfile

class Register(UserCreationForm):
    first_name= forms.CharField(max_length = 50, required=True)
    last_name= forms.CharField(max_length = 50, required=True)
    email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address', required=True)
    address = forms.CharField(max_length = 100, required=True)
    phone_number = PhoneNumberField(help_text='Enter your phone number with country code (i.e +23490xxxxxxx)', required=True)
    bank_name = forms.CharField(max_length=50, required=True)
    account_number = forms.IntegerField(required=True)
    account_name = forms.CharField(max_length=550, required=True)
    bio =  forms.CharField(widget=forms.Textarea, required=True)


    class meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email',   'password1',
                     'password2', 'address', 'phone_number')

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        
        except User.MultipleObjectsReturned:

            # A user was found with this as a username, raise an error.
            raise forms.ValidationError('This email address is already in use.')

class UserProfileForm(forms.ModelForm):
    class meta:
        model = UserProfile
        fields = ['address', 'phone_number', 'bio', 'bank_name', 'account_name', 'account_number' ]



# class Register(forms.Form):
#     first_name= forms.CharField(label="first_name", max_length = 50)
#     last_name= forms.CharField(label="last_name", max_length = 50)
#     email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address')

