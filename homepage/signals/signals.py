from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from transliterate import translit

from blog.models import Article
from shop.models import Category

def create_slug(instance, new_slug=None):
    try:
        translited_title = translit(instance.title, reversed=True)
    except:
        translited_title = instance.title
    Model = type(instance)
    slug = slugify(translited_title, True)
    if new_slug is not None:
        slug = new_slug
    qs = Model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


@receiver(pre_save, sender=Article)
@receiver(pre_save, sender=Category)
def pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)