from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product


def main(request):
    return render(request, 'mainapp/index.html', context={'user':request.user, 'title': 'interior'})


def products(request, pk=None):
    title = 'Products'
    links_menu = ProductCategory.objects.all()

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
            'products': products_list
        }

        return render(request, 'mainapp/products_list.html', context=context)

    products_category = ProductCategory.objects.all()
    return render(request, 'mainapp/products.html',
                  context={'title': 'products', 'links_menu': products_category})


def contacts(request):
    return render(request, 'mainapp/contacts.html', context={'title': 'contacts'})


def product(request, pk=None):
    links_menu = ProductCategory.objects.all()
    title = 'Product'

    product_entry = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': links_menu,
        'category': product_entry.category,
        'product': product_entry
    }
    return render(request, 'mainapp/product.html', context=context)
