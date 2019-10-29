from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from .utils import unique_slug_generator
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    phone_number = PhoneNumberField(blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    bank_name = models.CharField(max_length=50)
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=550)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    verified_email = models.BooleanField(default= False)

    

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("afrivent:user-dashboard", kwargs={"pk": self.pk})






class Event(models.Model):
    event_name = models.CharField("Enter name for Event", max_length=500)
    creator = models.ForeignKey(UserProfile, related_name='events_created', on_delete=models.CASCADE)
    address = models.TextField(max_length=5000)
    event_image = models.ImageField(upload_to='images')
    description = models.TextField(max_length=50000)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null= True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null= True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null= True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null= True)
    slug = models.SlugField(blank = True, null = True)  


    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse("afrivent:event-detail", kwargs={"slug": self.slug})



class EventTicket(models.Model):
    type = models.CharField("Enter a name for ticket", max_length=50)
    quantity = models.PositiveIntegerField(default = 1)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("EventTicket")
        verbose_name_plural = ("EventTickets")


    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("EventTicket_detail", kwargs ={"pk": self.pk})




def event_pre_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(event_pre_save, sender=Event)


