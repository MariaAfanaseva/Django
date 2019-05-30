from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from authapp.models import ShopUser
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm, OrderForm
from django.forms import inlineformset_factory
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F
from shop import settings
from adminapp.forms import ProductCategoryEditForm


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        if settings.DEBUG:
            db_profile_by_type(sender, 'UPDATE', connection.queries)


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductCategoryListView(IsSuperUserView, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Categories'
        return context

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(IsSuperUserView, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create category'
        return context


class ProductCategoryUpdateView(IsSuperUserView, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_custom:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update category'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                if settings.DEBUG:
                    db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class ProductCategoryDeleteView(IsSuperUserView, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete category'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(ProductCategory, pk=kwargs['pk'])
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UsersListView(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'Users'
        return context


class UsersCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'age', 'avatar'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Users create'
        return context


class UsersUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = 'username', 'first_name', 'last_name', 'age', 'email', 'password', 'is_active', 'avatar'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Users update'
        return context


class UsersDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_custom:users')

    def get_context_data(self, **kwargs):
        context = super(UsersDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'User delete'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(ShopUser, pk=kwargs['pk'])
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(IsSuperUserView, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Product'
        return context


class ProductCreateView(IsSuperUserView, CreateView):
    model = Product
    template_name = 'adminapp/product_create.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('admin_custom:products', kwargs={'pk': pk})

    def get_initial(self):
        initial_data = super(ProductCreateView, self).get_initial()
        initial_data['category'] = self.kwargs['pk']
        return initial_data

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['category'] = self.kwargs['pk']
        context['title'] = 'Product create'
        return context


class ProductUpdateView(IsSuperUserView, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('admin_custom:product_read', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Product update'
        return context


class ProductDeleteView(IsSuperUserView, DeleteView):
    model = Product
    template_name = 'adminapp/product_update.html'

    def get_success_url(self):
        self.object = self.get_object()
        pk = self.object.category.pk
        return reverse_lazy('admin_custom:products', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Product delete'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(Product, pk=kwargs['pk'])
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(IsSuperUserView, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Products'
        pk = self.kwargs['pk']
        context['category'] = ProductCategory.objects.filter(pk=pk).first()
        return context

    def get_queryset(self):
        pk =self.kwargs['pk']
        return Product.objects.all().filter(category__pk=pk)


class OrdersListView(ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Orders'
        return context

    def get_queryset(self):
        return Order.objects.all().order_by('-is_active')


class OrdersCreateView(IsSuperUserView, CreateView):
    model = Order
    # fields = []
    form_class = OrderForm
    success_url = reverse_lazy('adminapp:orders')
    template_name = 'adminapp/order_create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                             extra=5)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
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

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrdersDeleteView(IsSuperUserView, DeleteView):
    model = Order
    template_name = 'adminapp/order_delete.html'
    success_url = reverse_lazy('admin_custom:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Order delete'
        return context


class OrdersUpdateView(IsSuperUserView, UpdateView):
    model = Order
    template_name = 'adminapp/order_update.html'
    form_class = OrderForm
    success_url = reverse_lazy('admin_custom:orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                             extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)

        data['title'] = 'Order update'
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


class OrdersDetailView(IsSuperUserView, DetailView):
    model = Order
    template_name = 'adminapp/order_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Order'
        return context
