from rest_framework import serializers
from api.models import Customer,Product


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