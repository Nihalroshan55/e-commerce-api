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
    
    def perform_create(self, serializer):
        order_number = self.generate_order_number()
        serializer.save(order_number=order_number)

    def generate_order_number(self):
        last_order = Order.objects.last()
        if last_order:
            last_order_number = int(last_order.order_number[3:])
            new_order_number = last_order_number + 1
        else:
            new_order_number = 1

        return f'ORD{new_order_number:05d}'
    
    def get_queryset(self):
        queryset = Order.objects.all().select_related('customer').prefetch_related('order_item__product')

        products = self.request.query_params.get('products', None)
        customer_name = self.request.query_params.get('customer', None)

        if products:
            products_list = products.split(',')
            queryset = queryset.filter(order_item__product__name__in=products_list).distinct()

        if customer_name:
            queryset = queryset.filter(customer__name=customer_name)

        return queryset