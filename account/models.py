from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from afriventapp.models import UserProfile



def user_post_save(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(user_post_save, sender=User)