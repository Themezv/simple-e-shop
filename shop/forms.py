from django import forms
from shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'text_preview',
            'description',
            'available',
            'category',
            'relation',
            'avatar',
            'product_type',
        ]
