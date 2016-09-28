from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.TextField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("category", args=[str(self.slug)])

    def __str__(self):
        return self.name


class AbstractProduct(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.PositiveSmallIntegerField(blank=True)
    description = models.TextField(max_length=100)
    available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    relation = models.ManyToManyField('self', blank=True)
    avatar = models.ImageField(upload_to='items_avatars', default='kotenok.jpg' )

    def __str__(self):
        return self.name

    class META:
        abstract = True


class Product(AbstractProduct):
    def get_absolute_url(self):
        return reverse("product", args=[str(self.slug)])

    def __str__(self):
        return self.name


class Service(AbstractProduct):
    def get_absolute_url(self):
        return reverse("service", args=[str(self.name)])

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    # transliterate title
    # translit() takes first arg only unicode text
    # uni = unicode(instance.title)
    # translited_title = translit(uni, reversed=True)

    # Почему то все работает с русским текстом

    slug = slugify(instance.name, True)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_receiver, sender=Category)
pre_save.connect(pre_save_receiver, sender=Product)