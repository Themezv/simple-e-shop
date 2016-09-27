from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_items, name='all_items'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category, name='category'),
    url(r'^(?P<item>[\w-]+)/$', views.product, name='product'),
]