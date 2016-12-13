from django.contrib import admin
from shop.models import Category, Product, ProductType
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ['title','image', 'description', 'slug']


admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Product)
