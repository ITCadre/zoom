from django.db import models
#from datetime import datetime  
#from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User



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
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    do = models.ForeignKey(DiagramOwner, on_delete=models.CASCADE)
  


            