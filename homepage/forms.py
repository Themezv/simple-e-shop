from django import forms
from django.contrib.flatpages.models import FlatPage
from .models import Tiles
from ckeditor.widgets import CKEditorWidget


class AboutForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = [
            'title',
            'content'
        ]



class ContactForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = [
            'title',
            'content',
        ]
        widgets = {
            'title': CKEditorWidget(),
            'content': CKEditorWidget(),
        }


class TilesForm(forms.ModelForm):

    class Meta:
        model = Tiles
        fields = ('pages',)

