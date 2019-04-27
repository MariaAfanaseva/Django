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
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create category'
        return context


class ProductCategoryUpdateView(IsSuperUserView, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_custom:categories')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update category'
        return context


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






