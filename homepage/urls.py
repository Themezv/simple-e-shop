from django.conf.urls import url
from homepage.views import index, about_edit, contacts_edit, NewTileView, DeleteTileView
from django.contrib.flatpages.views import flatpage


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new_tile/$', NewTileView.as_view(), name='new_tile'),
    url(r'^tile-delete/$', DeleteTileView.as_view(), name='delete_tile'),
    url(r'^about/$', flatpage, {'url': '/about/'}, name='about'),
    url(r'^about/edit$', about_edit, name='about_edit'),
    url(r'^contacts/$', flatpage, {'url': '/contacts/'}, name='contacts'),
    url(r'^contacts/edit$', contacts_edit, name='contacts_edit'),
]
