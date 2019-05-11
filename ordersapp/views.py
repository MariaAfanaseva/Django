from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
   model = Order

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)

   def get_context_data(self, **kwargs):
       context = super(OrderList, self).get_context_data(**kwargs)
       context['title'] = 'Orders'
       return context
