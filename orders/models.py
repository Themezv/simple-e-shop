from django.core.urlresolvers import reverse
from django.db import models

from extuser.models import ExtUser
from shop.models import Product, Service


# Create your models here.


class OrderProduct(models.Model):
    user = models.ForeignKey(ExtUser)
    date = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, blank=True, null=True)
    count = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse("order_detail", args=[str(self.pk)])

    def __str__(self):
        return str(self.user.first_name)

    class Meta:
        verbose_name = "Заказ Товара"
        verbose_name_plural = "Заказы Товаров"


class OrderService(models.Model):
    user = models.ForeignKey(ExtUser)
    date = models.DateTimeField(auto_now_add=True)

    service = models.ForeignKey(Service, blank=True, null=True)

    def __str__(self):
        return str(self.user.first_name)

    def get_absolute_url(self):
        return reverse("order_detail", args=[str(self.pk)])

    class Meta:
        verbose_name = "Заказ Услуг"
        verbose_name_plural = "Заказы Услуг"
