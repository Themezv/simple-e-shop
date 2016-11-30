from django.core.urlresolvers import reverse
from django.db import models


from shop.models import Product, Service
# Create your models here.

class OrderedItem(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True)
    service = models.ForeignKey(Service, blank=True, null=True)
    count = models.PositiveSmallIntegerField(default=1) 

    def __str__(self):
        if self.product:
            return "Товар - %s:%s" %(self.product.name, self.count)
        if self.service:
            return "Услуга - %s:%s" %(self.service.name, self.count) 


class Order(models.Model):
    FIO = models.CharField(max_length=200)
    adress = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    items = models.ManyToManyField(OrderedItem)

    def get_absolute_url(self):
        return reverse("order_detail", args=[str(self.id)])

    def __str__(self):
        return str(self.FIO)
    