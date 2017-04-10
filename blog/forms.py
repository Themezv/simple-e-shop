from django import forms

from pagedown.widgets import PagedownWidget


from .models import Article
from shop.models import Category


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Article
        fields = [
            'title',
            'image',
            'category',
            'content',
            'draft',
        ]


class CategoryForm(forms.ModelForm):
    # content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Category
        fields = [
            'title',
            'image',
            'meta_description',
            # 'content',
            # 'draft',
        ]
