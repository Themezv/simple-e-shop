from django.contrib import admin
from .models import Article #, ArticleCategory


# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'image', 'draft','slug', 'category']



admin.site.register(Article, ArticlesAdmin)





