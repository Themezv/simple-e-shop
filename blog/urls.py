from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.article_list, name='article_list'),
    url(r'^create/$', views.article_create, name='article_create'),
    url(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='article_detail'),
    url(r'^(?P<slug>[\w-]+)/edit$', views.article_edit, name='article_edit'),
    url(r'^(?P<slug>[\w-]+)/delete$', views.article_delete, name='article_delete'),
]
