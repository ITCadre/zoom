'''
Created on Mar 8, 2016

@author: Waipang Fong
'''
from rest_framework import serializers
from zoom.models import Client, Customer, Device, DiagramOwner, Diagram

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields =  "__all__" 
        
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields =  "__all__" 
        
class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields =  "__all__" 
        
        
class DiagramOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiagramOwner
        fields =  "__all__"         
        
class DiagramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagram
        fields =  "__all__" 
        
