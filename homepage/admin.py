from django.contrib import admin
from homepage.models import MainSetting, ServiceTile, ProductTile
# Register your models here.

admin.site.register(MainSetting)
admin.site.register(ServiceTile)
admin.site.register(ProductTile)

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from ckeditor.widgets import CKEditorWidget


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)