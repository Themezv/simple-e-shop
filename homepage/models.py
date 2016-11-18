from django.db import models
from PIL import Image
from shop.models import Service


class Tiles(models.Model):
    pages = models.OneToOneField(Service, null=True)

    def __str__(self):
        return "Страницы для отображения на главной (плитки)"


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

