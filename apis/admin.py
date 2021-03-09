from django.contrib import admin
from apis.models import Product, Company, Menu, Tables, Order, OrderItem, Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Menu)
admin.site.register(Tables)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile, UserAdmin)


