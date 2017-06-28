from django.db import models
from django.core.urlresolvers import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import Article


class Manufacturer(models.Model):
    title = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class ProductManager(models.Manager):
    def items(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Item")

    def services(self, *args, **kwargs):
        return super(ProductManager, self).filter(product_type__title="Service")


class ProductGroup(models.Model):
    title = models.CharField('Название группы продукта', max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа продукта"
        verbose_name_plural = "Группы продуктов"


class ProductSubGroup(models.Model):
    group = models.ForeignKey(ProductGroup, verbose_name='Группа')
    title = models.CharField('Название подгруппы продукта', max_length=500)
    description = RichTextUploadingField('Описание подгруппы')

    def get_manufacturers(self):
        products = self.product_set.all()
        manufacturers = []
        for product in products:
            if product.manufacturer not in manufacturers:
                manufacturers.append(product.manufacturer)
        return manufacturers

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подгруппа продукта"
        verbose_name_plural = "Подгруппы продуктов"


class Currency(models.Model):
    title = models.CharField('Валюта', max_length=100)
    rate = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"


class Category(models.Model):
    title = models.CharField('Название категории', max_length=500, unique=True)
    meta_description = RichTextUploadingField('Описание', max_length=2000)
    slug = models.SlugField('Генерируется автоматически', unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category_image', null=True, blank=True)

    def has_articles(self):
        qs = Article.objects.all().filter(category=self)
        return qs.exists()

    def has_items(self):
        qs = Product.objects.items().filter(category=self)
        return qs.exists()

    def has_services(self):
        qs = Product.objects.services().filter(category=self)
        return qs.exists()

    def get_absolute_url(self):
        return reverse("product_categoried_list", args=[str(self.slug)])

    def get_absolute_url_for_blog(self):
        return reverse("article_list", args=[str(self.slug)])

    def get_absolute_url_for_service(self):
        return reverse("service_list", args=[str(self.slug)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    title = models.CharField('Название', max_length=200)
    avatar = models.ImageField('Изображение', upload_to='items_avatars')
    text_preview = RichTextUploadingField('Краткое описание', max_length=5000, null=True, blank=True)

    price = models.FloatField('Цена', blank=True, null=True)
    currency = models.ForeignKey(Currency, verbose_name='Валюта')

    description = RichTextUploadingField('Описание', max_length=10000)
    available = models.BooleanField(default=True)

    category = models.ManyToManyField(Category)
    relation = models.ManyToManyField('self', blank=True, symmetrical=True)
    subgroup = models.ForeignKey(ProductSubGroup, verbose_name='Подгруппа')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель')

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def get_category_slug(self):
        return self.category.first().slug

    def get_price_ruble(self):
        if self.currency.title == "RUB":
            return self.price
        elif self.currency.title == "USD":
            price = self.price * self.currency.rate
            return "%.2f" % price
        elif self.currency.title == "EUR":
            price = self.price * self.currency.rate
            return "%.2f" % price
        else:
            pass

    def get_price_usd(self):
        if self.currency.title == "USD":
            return self.price
        elif self.currency.title == "RUB":
            rate = Currency.objects.get(title="USD").rate
            price = self.price / rate
            return "%.2f" % price
        elif self.currency.title == "EUR":
            rate_ruble = self.currency.rate
            ruble_price = self.price * rate_ruble
            rate = Currency.objects.get(title="USD").rate
            price = ruble_price / rate
            return "%.2f" % price
        else:
            pass

    def get_price_eur(self):
        if self.currency.title == "EUR":
            return self.price
        elif self.currency.title == "RUB":
            rate = Currency.objects.get(title="EUR").rate
            price = self.price / rate
            return "%.2f" % price
        elif self.currency.title == "USD":
            rate_ruble = self.currency.rate
            ruble_price = self.price * rate_ruble
            rate = Currency.objects.get(title="EUR").rate
            price = ruble_price / rate
            return "%.2f" % price
        else:
            pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
