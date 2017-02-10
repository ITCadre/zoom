from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from zoom.models import Client, Customer, Device, DiagramOwner, Diagram


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def login(request, format=None):

    token = Token.objects.get(user = request.user)
    role = 'regular'
    if request.user.is_staff:
        role = 'staff'
    elif len(DiagramOwner.objects.filter(customer__user = request.user)) > 0:
        role = 'do'

    print (token.key)
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
        'token': token.key,
        'role' : role,


    }
    return Response(content)