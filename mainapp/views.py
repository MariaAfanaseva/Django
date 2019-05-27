from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product, ProductType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache


def get_products_type(type_product):
    if settings.LOW_CACHE:
        key = f'products_{type_product}'
        products_type = cache.get(key)
        if products_type is None:
            products_type = Product.objects.filter(type__name=type_product, is_active=True, category__is_active=True).select_related('type').order_by("?")
            cache.set(key, products_type)
        return products_type
    else:
        return Product.objects.filter(type__name=type_product, is_active=True, category__is_active=True).select_related('type').order_by("?")


def get_same_products(same_product):
    same_products = Product.objects.filter(category=same_product.category, is_active=True, category__is_active=True).exclude(pk=same_product.pk)
    return same_products


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)  # from cache
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)  # added in cache
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('type').order_by('price')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def main(request):
    exclusive_product = get_products_type('Exclusive')[:2]
    trending_products = get_products_type('Trending')[:6]
    types = ProductType.objects.all()
    same_products = get_same_products(exclusive_product.first())[:4]
    featured_products = get_products_type('Hot deal')[:4]

    context = {
        'user': request.user,
        'title': 'interior',
        'exclusive_product': exclusive_product,
        'trending_products': trending_products,
        'types': types,
        'same_products': same_products,
        'featured_products': featured_products,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None, num=None, page=1):
    title = 'Products'
    links_menu = get_links_menu()
    types = ProductType.objects.all()
    exclusive_product = get_products_type('Exclusive')[:2]

    if pk:
        if pk == '0':
            category = {'name': 'all', 'pk': 0}
            products_list = get_products()
        else:
            category = get_category(pk)
            products_list = Product.objects.filter(category__pk=pk).filter(is_active=True, category__is_active=True).select_related().order_by('price')

        paginator = Paginator(products_list, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'types': types,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    elif num:
        category = get_object_or_404(ProductType, pk=num)
        products_list = Product.objects.filter(type__pk=num).filter(is_active=True, category__is_active=True).select_related('type')
        context = {
            'title': 'products',
            'category': category,
            'links_menu': links_menu,
            'products': products_list,
            'exclusive_product': exclusive_product,
            'types': types,
        }

        return render(request, 'mainapp/products.html', context=context)


def contacts(request):
    types = ProductType.objects.all()
    context = {
        'title': 'contacts',

        'types': types,
    }
    return render(request, 'mainapp/contacts.html', context=context)


def product(request, pk=None):
    links_menu = get_links_menu()
    title = 'Product'

    product_entry = get_product(pk)
    same_product = get_same_products(product_entry)[:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': product_entry.category,
        'product': product_entry,
        'same_product': same_product,
    }
    return render(request, 'mainapp/product.html', context=context)
