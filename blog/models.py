from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from PIL import Image
from transliterate import translit


from homepage.models import create_slug, pre_save_receiver, pre_save_connect

# Create your models here.



class ArticleManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(ArticleManager, self).filter(draft=False)


class Article(models.Model):
    title = models.CharField(max_length=55, blank=True)
    content = models.TextField(max_length=50000, blank=True)
    published = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)
    # menu = models.BooleanField(default=False, help_text='Отображать в главном меню')
    # tile = models.BooleanField(default=False, help_text='Отображать на главной странице (плитка)')
    image = models.ImageField(upload_to='pages_avatars', blank=True)
    draft = models.BooleanField(default = False)

    objects = ArticleManager()

    # function return url for every object
    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.slug)])


    def __str__(self):
        return self.title


pre_save_connect(Article)