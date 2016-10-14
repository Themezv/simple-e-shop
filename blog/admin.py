from django.contrib import admin
from .models import Article


# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'image', 'draft']


admin.site.register(Article, ArticlesAdmin)






