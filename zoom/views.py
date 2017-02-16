from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from zoom.models import Client, Customer, Device, DiagramOwner, Diagram
from zoom.serializers import DiagramSerializer


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

    print ("waipang")
    
    diagrams = Diagram.objects.filter(diagram_owmer__customer__user__pk = pk)

    print (len(diagrams))
    serializer = DiagramSerializer(diagrams, many = True)
    #print(request.pk)
    
    
    return Response(serializer.data)


