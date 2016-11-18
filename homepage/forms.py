from django import forms
from django.contrib.flatpages.models import FlatPage
from .models import Tiles


class AboutForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = [
            'title',
            'content',
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = [
            'title',
            'content',
        ]


class TilesForm(forms.ModelForm):

    class Meta:
        model = Tiles
        fields = ('pages',)

