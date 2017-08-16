from django.db import models
from django.contrib.auth.models import User


class ExtUser(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    email = models.EmailField('email')
    phone = models.CharField('Номер телефона', max_length=20)
    # address = models.CharField(verbose_name="Адрес", max_length=200)

    def __str__(self):
        return str(self.email)
