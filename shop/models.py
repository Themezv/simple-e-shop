from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from transliterate import translit
    


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.TextField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category_image', null=True)

    def get_absolute_url(self):
        return reverse("product_list", args=[str(self.slug)])

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
    avatar = models.ImageField(upload_to='items_avatars')

    def __str__(self):
        return self.name

    def get_category_slug(self):
        return self.category.all().first().slug

    class META:
        abstract = True


class Product(AbstractProduct):
    def get_absolute_url(self):
        return reverse("product", args=[str(self.slug)])

    def __str__(self):
        return self.name


class Service(AbstractProduct):
    def get_absolute_url(self):
        return reverse("services", args=[str(self.name)])

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    try:
        translited_title = translit(instance.name, reversed=True)
    except:
        translited_title = instance.name
    Model = type(instance)
    slug = slugify(translited_title, True)
    if new_slug is not None:
        slug = new_slug
    qs = Model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


def pre_save_connect(Model):
    pre_save.connect(pre_save_receiver, sender=Model)


pre_save_connect(Product)
pre_save_connect(Service)
pre_save_connect(Category)
