from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image

from markdown_deux import markdown


class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ArticleManager, self).filter(draft=False)


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=500)
    image = models.ImageField()
    slug = models.SlugField(max_length=550, unique=True, blank=True)

    meta_description = models.CharField('SEO Описание', max_length=2000, blank=True, null=True)
    meta_title = models.CharField(verbose_name="SEO заголовок", max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('article_list', args=[str(self.slug)])

    def has_articles(self):
        return self.article_set.exists()


class Article(models.Model):
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    title = models.CharField(max_length=550)
    content = models.TextField(max_length=50000)
    published = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='article_image', blank=True)
    draft = models.BooleanField(default = False)

    meta_description = models.CharField('SEO Описание', max_length=2000, blank=True, null=True)
    meta_title = models.CharField(verbose_name="SEO заголовок", max_length=500, blank=True, null=True)

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
