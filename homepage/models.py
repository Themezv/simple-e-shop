from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from PIL import Image
from transliterate import translit
# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=55, blank=True)
    content = models.TextField(max_length=50000, blank=True)
    description = models.TextField(max_length=150, blank=True)
    published = models.DateTimeField(auto_now_add=True, null=True)  # Null ubrat'
    slug = models.SlugField(unique=True)
    menu = models.BooleanField(default=False, help_text='Отображать в главном меню')
    tile = models.BooleanField(default=False, help_text='Отображать на главной странице (плитка)')
    avatar = models.ImageField(upload_to='pages_avatars', blank=True)

    # function return url for every object
    def get_absolute_url(self):
        return reverse("page_detail", args=[str(self.slug)])

    def __str__(self):
        return self.title


def create_slug(instance, new_slug=None):
    try:
        translited_title = translit(instance.title, reversed=True)
    except:
        translited_title = instance.title
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


pre_save_connect(Page)



class MainSetting(models.Model):
    firm_name = models.CharField(max_length=70)
    phone1 = models.CharField(max_length=16)
    phone2 = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=100)
    work_time = models.TextField(max_length=100)
    logo = models.ImageField(upload_to='homepage')
    favicon = models.ImageField(upload_to='homepage', blank=True)
    active = models.BooleanField(default=False, help_text='Только одна запись должна быть активна')

    class META:
        unique_together = ("active",)
