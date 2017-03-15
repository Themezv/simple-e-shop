from django.db import models
from forex_python.converter import CurrencyRates
from django.core.urlresolvers import reverse



class ProductManager(models.Manager):
    def items(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Item")

    def services(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Service")


class ProductType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Currency(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=16, unique=True)
    description = models.TextField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category_image', null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product_categoried_list", args=[str(self.slug)])

    def get_absolute_url_for_blog(self):
        return reverse("article_list", args=[str(self.slug)])

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='items_avatars')
    text_preview = models.TextField(max_length=500, null=True, blank=True)

    price = models.PositiveSmallIntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency)

    description = models.TextField(max_length=100)
    available = models.BooleanField(default=True)

    category = models.ManyToManyField(Category)
    relation = models.ManyToManyField('self', blank=True, symmetrical=True)
    product_type = models.ForeignKey(ProductType)

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        if self.product_type.title == 'Item':
            return reverse("product_detail", args=[str(self.id)])

        if self.product_type.title == 'Service':
            return reverse("service_detail", args=[str(self.id)])

    def get_category_slug(self):
        return self.category.first().slug

    def get_price_ruble(self):
        if self.currency.title == "RUB":
            return self.price
        elif self.currency.title == "USD":
            c = CurrencyRates()
            rate = c.get_rate('USD', 'RUB')
            return "%.2f" %(self.price * rate)
        else:
            pass

    def get_price_usd(self):
        if self.currency.title == "USD":
            return self.price
        elif self.currency.title == "RUB":
            c = CurrencyRates()
            rate = c.get_rate('RUB', 'USD')
            return "%.2f" %(self.price * rate)
        else:
            pass

    def __str__(self):
        return self.title
