from rest_framework import serializers
from api.models import Customer,Product,OrderItem,Order
from django.utils import timezone

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact_number', 'email']
        extra_kwargs = {
            'name': {'validators': []},
        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'weight']
        extra_kwargs = {
            'name': {'validators': []},
        }
    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight must be a positive decimal and not more than 25kg.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']
        

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_items']
        extra_kwargs = {
            'order_number': {'read_only': True},
        }
    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value