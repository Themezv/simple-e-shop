from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image

from markdown_deux import markdown

from shop.models import Category


class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ArticleManager, self).filter(draft=False)


class Article(models.Model):
    title = models.CharField(max_length=55)
    content = models.TextField(max_length=50000)
    published = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='article_image', blank=True)
    draft = models.BooleanField(default = False)


    ##########FOREIGNFIELDS###########
    category = models.ForeignKey(Category)   


    objects = ArticleManager()

    # function return url for every object
    def get_category_slug(self):
        return self.category.slug

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.get_category_slug()), str(self.slug)])

    def get_markdown(self):
        return markdown(self.content)

    def __str__(self):
        return self.title


