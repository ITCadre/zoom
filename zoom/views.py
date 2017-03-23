from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from zoom.models import Client, Customer, Device, DiagramOwner, Diagram, Access, Application
from zoom.serializers import DiagramSerializer, ApplicationSerializer
from django.contrib.auth.models import User



import random

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def login(request, format=None):

    token = Token.objects.get(user = request.user)
    me = request.user
    role = 'regular'
    if request.user.is_staff:
        role = 'staff'
    elif len(DiagramOwner.objects.filter(customer__user = request.user)) > 0:
        role = 'do'
        me = DiagramOwner.objects.filter(customer__user = request.user)[0]

    print (token.key)
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
        'token': token.key,
        'role' : role,
        'pk'   : me.pk,


    }


    print (me.pk)  
    return Response(content)


@api_view(['GET'])
@permission_classes((AllowAny,))

def do_diagrams(request, pk):


    
    diagrams = Diagram.objects.filter(diagram_owmer__customer__user__pk = pk)

    print (len(diagrams))
    serializer = DiagramSerializer(diagrams, many = True)
    #print(request.pk)
    
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))

def get_application(request, pk):


    
    application = Application.objects.filter(pk = pk)[0]


    serializer = ApplicationSerializer(application)
    #print(request.pk)
    
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def device_applications(request, pk):

    print("hello") 
    applications = Application.objects.filter(device__pk = pk)

    print (len(applications))
    serializer = ApplicationSerializer(applications, many = True)
    #print(request.pk)
    
    content = {
        'myname': "hello",  
  
        }
        
    return Response(serializer.data)
    #return Response(content)
@api_view(['POST'])
@permission_classes((AllowAny,))

def assign_user_to_diagram(request):

    user_name = request.data.get('username')
    do_id = request.data.get('do') 
    print (user_name)
    print (do_id)


    user_set  =  User.objects.filter(username = user_name)

    if len(user_set) == 0:
        print ("create this user")
        myuser = User(username= user_name, password = "zoomzoom")


        do = DiagramOwner.objects.filter(pk = do_id)[0]

        client  = do.customer.client

        myuser.save()
        c = Customer(user = myuser, client = client)
        c.save()

        

        ran = random.randint(1000, 9999)

        access = Access(customer = c, do = do, temp_key = ran  )


        access.save()

        content = {
        'temp_key': ran,  
  
        }
        




    else:
        print ("what i am gonna do with you")    
        content = {
        'myname': "hello",  
  
        }
        

    


    return Response(content)