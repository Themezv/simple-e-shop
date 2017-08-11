from django.contrib import admin
from .models import Article, Category  #, ArticleCategory


# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'image', 'draft','slug', 'category']


admin.site.register(Article, ArticlesAdmin)
admin.site.register(Category)





