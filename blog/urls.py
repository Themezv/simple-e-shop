from django.conf.urls import url

from . import views
from .views import CategoryListView, ArticleListView, ArticleCreateView, ArticleDetail

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<category_slug>[\w-]+)/$', ArticleListView.as_view(), name='article_list'),
    url(r'^(?P<category_slug>[\w-]+)/create/$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', ArticleDetail.as_view(), name='article_detail'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<article_slug>[\w-]+)/edit$', views.article_edit, name='article_edit'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<article_slug>[\w-]+)/delete$', views.article_delete, name='article_delete'),
]
