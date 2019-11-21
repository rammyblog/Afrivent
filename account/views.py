from django.shortcuts import render, get_object_or_404, redirect
from account.forms import Register, UserProfileForm
from afriventapp.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,  logout
from .tokens import account_activation_token
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


def user_register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            # Get all info from form
            user.email =  form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name=  form.cleaned_data['last_name']
            
            

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            to_email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            user_bio = form.cleaned_data['bio']
            acct_number = form.cleaned_data ['account_number']
            acct_name = form.cleaned_data ['account_name']
            bank_name = form.cleaned_data ['bank_name']
    
            user.is_active = False
            user.save()

            UserProfile.objects.create(
                user = user,
                address = address,
                phone_number =  phone_number,
                bio = user_bio,
                bank_name = bank_name,
                account_number = acct_number,
                account_name = acct_name
            )


            # Sending mail 
            current_site = get_current_site(request)
            mail_subject = "Activate Your Afrivent Account!"
            message = render_to_string(
                'account/activate_email.html', {
                    'user': user,
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : account_activation_token.make_token(user)
                })
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            print('Send')
            return HttpResponse('Please confirm your email address to complete the registration')
            # auth_login(request, username, password)
            # print(request.u)

            # return redirect('afrivent:home')


    else:
        form = Register()

    context = {'form': form}

    return render(request, 'registration/register.html', context)

def activate_account(request, uidb64, token):
    # uid = force_text(urlsafe_base64_decode(uidb64))

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        print(uid)
        user.is_active = True
        print(user)
        profile = get_object_or_404(UserProfile, user=user)
        # profile = UserProfile.objects.get(user=user.username)
        profile.verified_email = True
        user.save()
        profile.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            auth_login(request, username, password)
        except AttributeError:
            return HttpResponse('Check your mail for a verification mail!')

            
        return redirect('afrivent:home')


    context = {}
    return render(request, 'registration/login.html', context)


def user_logout(request):
    messages.add_message(request, messages.INFO, 'Logged Out Successfully')
    print(messages)
    logout(request) 
    return redirect('afrivent:home')


def auth_login(request, username, password):
        user = authenticate(request, username=username, password=password)
        login(request, user)   



# def user_register(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
            

#     else:
#         form = UserProfileForm()

#     context = {'form': form}

#     return render(request, 'account/register.html', context)