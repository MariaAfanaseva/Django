from django.conf.urls import url
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    url(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
]
