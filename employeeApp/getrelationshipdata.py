from rest_framework import viewsets
from .models import *
from .serializers import *

def addressDetails(addrId):
        queryset = Address.objects.filter(registartionid=addrId)
        serializer = UserSerializer(queryset, many=True)
        return serializer.data