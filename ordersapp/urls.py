from django.conf.urls import url
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    url(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
    url(r'^order/create/$', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    url(r'^order/update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    url(r'^order/delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),
]
