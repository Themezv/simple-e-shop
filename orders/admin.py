from django.contrib import admin

from orders.models import OrderedItem, Order
# Register your models here.

admin.site.register(OrderedItem)
admin.site.register(Order)