from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.category_list, name='category_list'),
    url(r'^(?P<category_slug>[\w-]+)/$', views.article_categoried_list, name='article_categoried_list'),
    url(r'^(?P<category_slug>[\w-]+)/create/$', views.article_create, name='article_create'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<article_slug>[\w-]+)/$', views.article_detail, name='article_detail'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<article_slug>[\w-]+)/edit$', views.article_edit, name='article_edit'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<article_slug>[\w-]+)/delete$', views.article_delete, name='article_delete'),
]
