from django.conf.urls import url
from .views import (ProductListView,
                    ProductDetailView,
                    FilteredProductListView,
                    ServiceListView, ServiceDetailView)
    # , CategoryServiceListView, ServiceDetailView, ProductCreateView

urlpatterns = [
    url(r'^shop/$', ProductListView.as_view(), name='product_list'),
    url(r'^shop/filter$', FilteredProductListView.as_view(), name='filtered_product_list'),
    url(r'^shop/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product_detail'),

    #    url(r'^shop/create_product/$', ProductCreateView.as_view(), name='product_create'),

    url(r'^service/$', ServiceListView.as_view(), name='service_list'),
    url(r'^service/(?P<pk>[\w-]+)/$', ServiceDetailView.as_view(), name='service_detail'),
    #   url(r'^service/view/(?P<pk>[\d]+)/$', ServiceDetailView.as_view(), name='service_detail'),
]
