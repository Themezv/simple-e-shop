from django.db import models
from PIL import Image
from shop.models import Product


class Tiles(models.Model):
    pages = models.OneToOneField(Product, null=True)

    def __str__(self):
        return "Страницы для отображения на главной (плитки)"


class MainSetting(models.Model):
    firm_name = models.CharField('Название компании', max_length=70)
    phone1 = models.CharField('Номер телефона', max_length=16)
    phone2 = models.CharField('Номер телефона', max_length=16, blank=True)
    address = models.TextField('Адрес', max_length=100,)
    work_time = models.TextField('Время работы', max_length=100)
    logo = models.ImageField('Логотип', upload_to='homepage')
    favicon = models.ImageField('Маленькая иконка сайта во вкладке', upload_to='homepage', blank=True)
    active = models.BooleanField(default=False, help_text='Только одна запись должна быть активна')

    class META:
        unique_together = ("active",)

    def __str__(self):
        return "Главные настройки сайта. Информация в верхней части"
