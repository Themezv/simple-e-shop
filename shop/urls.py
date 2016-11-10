from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^shop/$', views.product_list, name='product_list'),
    url(r'^shop/filter/category_list/$', views.category_list, name='category_list'),
    url(r'^shop/filter/(?P<category_slug>[\w-]+)/$', views.product_categoried_list, name='product_categoried_list'),
    url(r'^shop/(?P<product_slug>[\w-]+)/$', views.product_detail, name='product_detail'),
    url(r'^service/$', views.service_list, name='service_list'),
    url(r'^service/(?P<service_slug>[\w-]+)/$', views.service_detail, name='service_detail'),
]