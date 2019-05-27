from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product, ProductType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache


def get_product(type_product):
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


def main(request):
    exclusive_product = get_product('Exclusive')[:2]
    trending_products = get_product('Trending')[:6]
    types = ProductType.objects.all()
    same_products = get_same_products(exclusive_product.first())[:4]
    featured_products = get_product('Hot deal')[:4]

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
    exclusive_product = get_product('Exclusive')[:2]

    if pk:
        if pk == '0':
            category = {'name': 'all', 'pk': 0}
            products_list = Product.objects.select_related('type').filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
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

    product_entry = get_object_or_404(Product, pk=pk)
    same_product = get_same_products(product_entry)[:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': product_entry.category,
        'product': product_entry,
        'same_product': same_product,
    }
    return render(request, 'mainapp/product.html', context=context)
