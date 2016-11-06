from django.conf.urls import url

from homepage.views import index

from django.contrib.flatpages.views import flatpage


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', flatpage, {'url': '/about/'}, name='about'),
    url(r'^contacts/$', flatpage, {'url': '/contacts/'}, name='contacts'),
]
