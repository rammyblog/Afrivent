from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name='login'),
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logouts', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate_account')
]