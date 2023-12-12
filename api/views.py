# from django.shortcuts import render
from rest_framework import viewsets
from api.models import Customer,Product
from api.serializer import CustomerSerializer,ProductSerializer

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer