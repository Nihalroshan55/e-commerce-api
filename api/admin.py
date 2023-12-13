from django.contrib import admin

# Register your models here.
from .models import Customer, Product, Order, OrderItem

admin.site.register(Customer, list_display=('id', 'name', 'contact_number', 'email'))
admin.site.register(Product, list_display=('id', 'name', 'weight'))
admin.site.register(Order, list_display=('id', 'order_number', 'customer', 'order_date', 'address'))
admin.site.register(OrderItem, list_display=('id', 'order', 'product', 'quantity'))