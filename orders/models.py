from django.core.urlresolvers import reverse
from django.db import models


from shop.models import Product
# Create your models here.


class OrderedItem(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True)
    count = models.PositiveSmallIntegerField('Количество', default=1)

    def __str__(self):
        return "%s:Название-%s, количество-%s" % (self.product.product_type.title, self.product.title, self.count)

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"


class Order(models.Model):
    FIO = models.CharField('Фамилия Имя Отчество',max_length=500)
    address = models.CharField('Адрес', max_length=500)
    email = models.EmailField('E-mail')
    phone_number = models.CharField('Номер телефона', max_length=20)
    items = models.ManyToManyField(OrderedItem)
    timestamp = models.DateTimeField('Время заказа', auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse("order_detail", args=[str(self.id)])

    def __str__(self):
        return str(self.FIO)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
