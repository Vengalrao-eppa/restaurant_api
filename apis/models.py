from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    phone=models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Company(models.Model):
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default = True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Tables(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    menu = models.ManyToManyField(Menu)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    created_date = models.DateTimeField(editable=False, auto_now_add=True)
    order_id = models.CharField(max_length = 25, editable=False)

    def __str__(self):
        return self.user.get_full_name() + ' ' + self.order_id

    def save(self, *args, **kwargs):
        if not self.id:
            self.order_id = datetime.now().strftime('%d%m%Y%H%M%S')
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    products =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    def __str__(self):
        return self.products.name + ' ' + self.order.order_id
