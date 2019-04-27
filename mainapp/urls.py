from django.conf.urls import url
import mainapp.views as mainapp

app_name = 'mainapp'


urlpatterns = [
    url(r'^(?P<num>\d+)$', mainapp.products, name='index'),
    url(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
    url(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='page'),
    url(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
]


