from django.contrib import admin

from orders.models import OrderService, OrderProduct
# Register your models here.

admin.site.register(OrderService)
admin.site.register(OrderProduct)