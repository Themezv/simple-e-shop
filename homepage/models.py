from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image


class Page(models.Model):
    title = models.CharField(max_length=55, blank=True)
    content = models.TextField(max_length=50000, blank=True)
    description = models.TextField(max_length=150, blank=True)
    published = models.DateTimeField(auto_now_add=True, null=True)  # Null ubrat'
    slug = models.SlugField(unique=True, blank=True)
    menu = models.BooleanField(default=False, help_text='Отображать в главном меню')
    tile = models.BooleanField(default=False, help_text='Отображать на главной странице (плитка)')
    avatar = models.ImageField(upload_to='pages_avatars', blank=True)

    # function return url for every object
    def get_absolute_url(self):
        return reverse("page_detail", args=[str(self.slug)])

    def __str__(self):
        return self.title


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

