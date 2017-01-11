from django import forms
from shop.models import Product
from orders.models import OrderedItem, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'FIO',
            'address',
            'phone_number',
            'email',
            # 'items',
        ]
