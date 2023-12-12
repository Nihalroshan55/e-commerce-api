# from django.shortcuts import render
from rest_framework import viewsets
from api.models import Customer
from api.serializer import CustomerSerializer

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer