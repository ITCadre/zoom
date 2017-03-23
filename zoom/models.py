from django.db import models
#from datetime import datetime  
#from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Client(models.Model):
    name = models.CharField(max_length=200)


class Customer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Device(models.Model):
    uid = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)




class DiagramOwner(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Diagram(models.Model):
    diagram_type = models.CharField(max_length=200) 
    name = models.CharField(max_length=200) 
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    diagram_owmer = models.OneToOneField(
        DiagramOwner,
        on_delete=models.CASCADE,
        primary_key=True,
    )

class Access(models.Model):    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null = True)
    do = models.ForeignKey(DiagramOwner, on_delete=models.CASCADE)
    temp_key = models.IntegerField(default =0)


    
class Application(models.Model):    
    name  = models.CharField(max_length=200) 
    content = models.TextField(blank = True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null = True)
  





            