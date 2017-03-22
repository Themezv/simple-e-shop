from django import forms
from shop.models import Product
from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'currency',
            'price',
            'text_preview',
            'description',
            'available',
            'category',
            'relation',
            'avatar',
            'product_type',
        ]
