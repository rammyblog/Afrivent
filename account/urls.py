from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate_account'),
    
]