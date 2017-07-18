from django.db.models import Manager


class ProductManager(Manager):
    def active(self, *args, **kwargs):
        return super(ProductManager, self).filter(available=True)
