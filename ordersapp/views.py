from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from ordersapp.forms import OrderItemForm, OrderForm
from django.db import transaction
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.http import JsonResponse
from mainapp.models import Product
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Orders'
        return context

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                             extra=3)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all()

            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price

            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        data['title'] = 'Order products'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                self.request.user.basket.all().delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderRead(DetailView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'Order view'
        return context


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Order update'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                             extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            # formset = OrderFormSet(instance=self.object)
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Order delete'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})


@receiver(pre_save, sender=OrderItem)
# @receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity = F('quantity') - instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
# @receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity = F('quantity') + instance.quantity
    instance.product.save()
