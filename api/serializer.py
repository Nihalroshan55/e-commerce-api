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
        fields = ['id','product', 'quantity']
        

class OrderSerializer(serializers.ModelSerializer):
    order_item= OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_item']
        extra_kwargs = {
            'order_number': {'read_only': True},
        }
    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value
    
    def validate(self, data):
        order_items_data = data.get('order_item', [])

        # Validate cumulative weight of order items
        total_weight = sum(item['product'].weight * item['quantity'] for item in order_items_data) # calculating total wait of the order_item 
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")

        return data
    
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_item', [])
        order = Order.objects.create(**validated_data)
        
        order_items = order_items_data 
        for order_item_data in order_items:
            OrderItem.objects.create(order=order, **order_item_data)

        return order
    
    def update(self, instance, validated_data):
        order_item_data = validated_data.pop('order_item', [])  

        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        instance.order_item.all().delete()
        for order_item_data in order_item_data:
            OrderItem.objects.create(order=instance,**order_item_data)

        return instance