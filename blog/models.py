from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image


class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ArticleManager, self).filter(draft=False)


class Article(models.Model):
    title = models.CharField(max_length=55, blank=True)
    content = models.TextField(max_length=50000, blank=True)
    published = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='article_image', blank=True)
    draft = models.BooleanField(default = False)

    objects = ArticleManager()

    # function return url for every object
    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.slug)])

    def __str__(self):
        return self.title
