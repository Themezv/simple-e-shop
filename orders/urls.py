from django.conf.urls import url

from .views import OrderListView, OrderDetailView, OrderCreateView


urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='order_list'),
    url(r'^(?P<pk>[0-9]+)/$', OrderDetailView.as_view(), name='order_detail'),
    url(r'^order-create/$', OrderCreateView.as_view(), name='order_create'),
]
