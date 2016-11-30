from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.order_list, name='order_list'),
    url(r'^(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^order-create/$', views.order_create, name='order_create'),
]
