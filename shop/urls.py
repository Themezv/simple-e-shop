from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.in_work, name='in_work'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category, name='category'),
    url(r'^(?P<cat>[\w-]+)/(?P<item>[\w-]+)/$', views.product, name='product'),
]