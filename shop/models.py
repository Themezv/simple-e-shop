from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from transliterate import translit


class ProductManager(models.Manager):
    def items(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Item")

    def services(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Service")


class ProductType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=16, unique=True)
    description = models.TextField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category_image', null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product_categoried_list", args=[str(self.slug)])

    def get_absolute_url_for_blog(self):
        return reverse("article_list", args=[str(self.slug)])

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=20)
    price = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(max_length=100)
    available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    relation = models.ManyToManyField('self', blank=True, symmetrical=True)
    avatar = models.ImageField(upload_to='items_avatars')
    text_preview = models.TextField(max_length=500, null=True, blank=True)

    # ForeignKey
    product_type = models.ForeignKey(ProductType)

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        if self.product_type.title == 'Item':
            return reverse("product_detail", args=[str(self.id)])

        if self.product_type.title == 'Service':
            return reverse("service_detail", args=[str(self.id)])

    def get_category_slug(self):
        return self.category.first().slug

    def __str__(self):
        return self.title
