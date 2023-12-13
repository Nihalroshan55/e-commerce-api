# from django.shortcuts import render
from rest_framework import viewsets,filters
from api.models import Customer,Product,Order
from api.serializer import CustomerSerializer,ProductSerializer,OrderSerializer
from django.db.models import Q

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    # Adding order_number automaticlly to the order 
    def perform_create(self, serializer):
        order_number = self.generate_order_number() # Creating order_number using function generate_order_number
        serializer.save(order_number=order_number)

    def generate_order_number(self):
        last_order = Order.objects.last() # Getting the last order 
        if last_order:
            last_order_number = int(last_order.order_number[3:]) # Extracting order number form the order 
            new_order_number = last_order_number + 1   # Adding one to the last order number to get consecutive order_number
        else:
            new_order_number = 1  # if there is no order number start from 1 
            
        # returning the order_number that we get and converting in to the format ORDXXXXX (at least 5 zeros)
        return f'ORD{new_order_number:05d}' 
    
    def get_queryset(self):
        # Getting all orders and eagerly load related data (customer and associated products)
        queryset = Order.objects.all().select_related('customer').prefetch_related('order_item__product')

        # Getting query parameters from the request
        products = self.request.query_params.get('products', None)
        customer_name = self.request.query_params.get('customer', None)

        if products:
            products_list = products.split(',') # spliting the product if there is more than one 
            queryset = queryset.filter(order_item__product__name__in=products_list).distinct()

        if customer_name:
            queryset = queryset.filter(customer__name=customer_name)

        return queryset

