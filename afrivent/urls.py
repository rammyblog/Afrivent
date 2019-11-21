"""afrivent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings    
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('afriventapp.urls')),
    path('order/', include('order.urls')),
    path('accounts/reset', auth_views.PasswordResetView.as_view(
       template_name = 'account/password_reset_form.html', email_template_name = 'account/password_reset_email.html', subject_template_name = 'account/password_reset_subject.txt' ), 
    name = 'password_reset'
    ),
    path('accounts/reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name = 'account/password_reset_done.html'
        ), name = 'password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'account/password_reset_confirm.html'),
    name = 'password_reset_confirm'),


    path('accounts/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
    name='password_reset_complete'), 

   path('accounts/settings/password/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),
    name='password_change'),

   path('accounts/settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='account/password_change_done.html'),
    name='password_change_done'
    ),
    path('accounts/', include('account.urls')),


    # path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)