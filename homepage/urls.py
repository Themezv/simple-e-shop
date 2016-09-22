from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[\w-]+)/$', views.page_detail, name='page_detail'),
    url(r'^page/create/$', views.page_create, name='page_create'),
    url(r'^(?P<slug>[\w-]+)/edit$', views.page_edit, name='page_edit'),
    url(r'^(?P<slug>[\w-]+)/delete$', views.page_delete, name='page_delete'),

]
