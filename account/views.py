from django.shortcuts import render, get_object_or_404, redirect
from account.forms import Register, UserProfileForm
from afriventapp.models import UserProfile

from django.contrib.auth import authenticate, login,  logout

from django.contrib import messages


def user_register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.email =  form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name=  form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            user.save()
            auth_login(request, username, password)
            # print(request.u)
            profile = UserProfile.objects.get(user=request.user)
            profile.address = address
            profile.phone_number = phone_number
            profile.save()
            return redirect('afrivent:home')


    else:
        form = Register()

    context = {'form': form}

    return render(request, 'account/register.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_login(request, username, password)
        return redirect('afrivent:home')


    context = {}
    return render(request, 'account/signIn.html', context)


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