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
