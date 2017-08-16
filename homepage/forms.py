from django import forms
from django.contrib.flatpages.models import FlatPage
from .models import ProductTile, ServiceTile
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AboutForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

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
            'title': CKEditorUploadingWidget(config_name='awesome_ckeditor'),
            'content': CKEditorUploadingWidget(config_name='awesome_ckeditor'),
        }


class ServiceTileForm(forms.ModelForm):

    class Meta:
        model = ServiceTile
        fields = ('pages',)


class ProductTileForm(forms.ModelForm):
    class Meta:
        model = ProductTile
        fields = ('pages',)

