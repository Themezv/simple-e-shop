from django.conf.urls import url
from .views import ItemListView, ServiceListView, CategoryShopListView, ItemCategoriedListView, ItemDetailView, ServiceDetailView, ProductCreateView


urlpatterns = [
    url(r'^shop/$', ItemListView.as_view(), name='product_list'),
    url(r'^shop/create_product/$', ProductCreateView.as_view(), name='product_create'),
    url(r'^shop/filter/category_list/$', CategoryShopListView.as_view(), name='category_list'),
    url(r'^shop/filter/(?P<category_slug>[\w-]+)/$', ItemCategoriedListView.as_view(), name='product_categoried_list'),
    url(r'^shop/(?P<pk>[0-9]+)/$', ItemDetailView.as_view(), name='product_detail'),
    url(r'^service/$', ServiceListView.as_view(), name='service_list'),
    url(r'^service/(?P<pk>[\d]+)/$', ServiceDetailView.as_view(), name='service_detail'),
]
