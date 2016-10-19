from django.contrib import admin
from shop.models import Category, AbstractProduct, Product, Service
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name','image', 'description', 'slug']


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)