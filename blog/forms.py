from django import forms

from pagedown.widgets import PagedownWidget


from .models import Article


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
