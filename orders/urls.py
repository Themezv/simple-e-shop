from django.conf.urls import url

from orders.views import ServiceOrderCreate, ProductOrderCreate, OrdersListView

urlpatterns = [
    url(r'^$', OrdersListView.as_view(), name='orders_list'),
#     url(r'^(?P<pk>[0-9]+)/$', OrderDetailView.as_view(), name='order_detail'),

    url(r'^order-create/service$', ServiceOrderCreate.as_view(), name='service_order_create'),
    url(r'^order-create/product', ProductOrderCreate.as_view(), name='product_order_create'),
]
