from django.db import models
from django.core.urlresolvers import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from blog.models import Article
from shop.managers import ProductManager


class Manufacturer(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('Генерируется автоматически', unique=True, null=True, blank=True)

    def get_request_part(self):
        return "manufacturer=%s&" % self.slug

    def get_absolute_url(self):
        url = reverse("filtered_product_list")
        return url + "?" + self.get_request_part()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class ProductGroup(models.Model):
    title = models.CharField('Название группы товаров', max_length=500)
    image = models.ImageField(verbose_name="Изображение", null=True, blank=True)
    slug = models.SlugField('Генерируется автоматически', unique=True, null=True, blank=True)

    meta_description = models.CharField('SEO Описание', max_length=2000, blank=True, null=True)
    meta_title = models.CharField(verbose_name="SEO заголовок", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_all_categories(self):
        products = self.product_set.active()
        qs = Category.objects.filter(product__in=products).distinct()
        return qs

    def get_all_manufacturers(self):
        products = self.product_set.active()
        qs = Manufacturer.objects.filter(product__in=products).distinct()
        return qs

    def get_request_part(self):
        return "group=%s&" % self.slug

    class Meta:
        verbose_name = "Группа товаров"
        verbose_name_plural = "Группы товаров"


class Currency(models.Model):
    title = models.CharField('Валюта', max_length=100)
    rate = models.FloatField()

    def __str__(self):
        return self.title

    def convert_to_curr(self, cur):
        return self.rate/Currency.objects.get(title=cur).rate

    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"


class Category(models.Model):
    title = models.CharField('Название категории', max_length=500, unique=True)
    description = RichTextUploadingField('Описание', max_length=5000)
    slug = models.SlugField('Генерируется автоматически', unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category_image', null=True, blank=True)

    meta_description = models.CharField('SEO Описание', max_length=2000, blank=True, null=True)
    meta_title = models.CharField(verbose_name="SEO заголовок", max_length=500, blank=True, null=True)

    def get_request_part(self):
        return "category=%s&" % self.slug

    def get_absolute_url(self):
        url = reverse("filtered_product_list")
        return url + "?" + self.get_request_part()

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
    new_price = models.FloatField("Цена со скидкой", blank=True, null=True)
    currency = models.ForeignKey(Currency, verbose_name='Валюта')

    description = RichTextUploadingField('Описание', max_length=10000)
    available = models.BooleanField(verbose_name="Доступ", default=True)

    category = models.ManyToManyField(Category, verbose_name="Категория")
    relation = models.ManyToManyField('self', blank=True, symmetrical=True)

    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель')
    group = models.ForeignKey(ProductGroup, verbose_name="Группа товаров")

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def get_category_slug(self):
        return self.category.first().slug

    def get_price_ruble(self):
        return self.price * self.currency.convert_to_curr('RUB')

    def get_price_usd(self):
        return self.price * self.currency.convert_to_curr('USD')

    def get_price_eur(self):
        return self.price * self.currency.convert_to_curr('EUR')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Service(models.Model):
    class Meta:
        verbose_name_plural = "Услуги"
        verbose_name = "Услуга"

    title = models.CharField(verbose_name="Название", max_length=500)
    description = RichTextUploadingField('Описание', max_length=10000)

    text_preview = models.CharField(verbose_name='Краткое описание', max_length=1000, null=True, blank=True)

    meta_title = models.CharField(verbose_name="SEO заголовок", max_length=500)
    meta_description = models.CharField(verbose_name="SEO описание", max_length=5000)

    image = models.ImageField(verbose_name="Изображение")

    price = models.FloatField(verbose_name="Цена", blank=True, null=True)
    new_price = models.FloatField(verbose_name="Цена со скидкой", blank=True, null=True)

    available = models.BooleanField(verbose_name="Доступ", default=True)

    currency = models.ForeignKey(Currency, blank=True, null=True)

    group = models.ForeignKey(ProductGroup, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("service_detail", args=[str(self.pk)])

    def __str__(self):
        return str(self.title)