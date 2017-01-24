from django.conf.urls import url

from .views import CategoryListView, ArticleListView, ArticleCreateView, ArticleDetail, ArticleEditView, ArticleDeleteView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='article_category_list'),
    url(r'^(?P<category_slug>[\w-]+)/$', ArticleListView.as_view(), name='article_list'),
    url(r'^(?P<category_slug>[\w-]+)/create/$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', ArticleDetail.as_view(), name='article_detail'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/edit$', ArticleEditView.as_view(), name='article_edit'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/delete$', ArticleDeleteView.as_view(), name='article_delete'),
]
