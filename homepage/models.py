from django.db import models
from PIL import Image
# Create your models here.


class Page(models.Model):
    name = models.CharField(max_length=15, unique=True)
    title = models.TextField(max_length=55)
    description = models.TextField(max_length=150)
    lable = models.CharField(max_length=20, unique=True)
    menu = models.BooleanField(default=False, help_text='Отображать в главном меню')
    tile = models.BooleanField(default=False, help_text='Отображать на главной странице (плитка)')
    avatar = models.ImageField(upload_to='pages_avatars', blank=True)

    def __str__(self):
        return self.name


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
