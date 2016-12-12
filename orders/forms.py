from django import forms


from shop.models import Product
from orders.models import OrderedItem, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'FIO',
            'adress',
            'phone_number',
            'email',
            # 'items',
        ]
