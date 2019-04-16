from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket


def get_hot_product():
    return Product.objects.filter(exclusive=False).order_by("?").first()


def get_exclusive_product():
    return Product.objects.filter(exclusive=True)[:2]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


def main(request):
    basket = {}
    if not request.user.is_anonymous:
        basket = Basket.objects.filter(user=request.user)

    exclusive_product = get_exclusive_product()

    context = {
        'user': request.user,
        'title': 'interior',
        'basket': basket,
        'exclusive_product': exclusive_product,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    title = 'Products'
    links_menu = ProductCategory.objects.all()
    basket = {}
    if not request.user.is_anonymous:
        basket = Basket.objects.filter(user=request.user)

    if pk:
        if pk == '0':
            category = {'name': 'all'}
            products_list = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_list,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    products_category = ProductCategory.objects.all()
    hot_product = get_hot_product()
    exclusive_product = get_exclusive_product()
    same_product = get_same_products(hot_product)
    context = {
        'title': 'products',
        'links_menu': products_category,
        'hot_product': hot_product,
        'same_product': same_product,
        'exclusive_product': exclusive_product,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context=context)


def contacts(request):
    basket = {}
    if not request.user.is_anonymous:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': 'contacts',
        'basket': basket,
    }
    return render(request, 'mainapp/contacts.html', context=context)


def product(request, pk=None):
    links_menu = ProductCategory.objects.all()
    title = 'Product'
    basket = {}
    if not request.user.is_anonymous:
        basket = Basket.objects.filter(user=request.user)

    product_entry = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': product_entry.category,
        'product': product_entry,
        'basket': basket,
    }
    return render(request, 'mainapp/product.html', context=context)
