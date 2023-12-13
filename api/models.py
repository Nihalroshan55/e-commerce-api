from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"
