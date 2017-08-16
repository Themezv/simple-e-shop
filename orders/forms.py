from django import forms


class OrderForm(forms.Form):
    count = forms.FloatField(max_value=5000, required=False)
    count.label = "Количество"

    item_id = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, required=True)
    item_id.label = "ID"
