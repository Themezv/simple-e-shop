from django import forms

from extuser.models import ExtUser


class ExtUserForm(forms.ModelForm):
    class Meta:
        fields = ['first_name', 'last_name', 'email', "phone", "address"]
        model = ExtUser

    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Имя"}))
    first_name.label = "Имя"

    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Фамилия"}))
    last_name.label = "Фамилия"

    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Фамилия"}))
    address.label = "Адрес"

    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Номер телефона",
                                                          "pattern": ".{10, 25}",
                                                          "type": "tel"}))
    phone.label = "Номер телефона"

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "E-mail"}))
    email.label = "E-mail"

