from django.contrib import admin
from shop.models import Category, Product, ProductSubGroup, Currency, ProductGroup, Manufacturer

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'description', 'slug']


admin.site.register(Manufacturer)
admin.site.register(ProductGroup)
admin.site.register(Category)
admin.site.register(ProductSubGroup)
admin.site.register(Product)
admin.site.register(Currency)
