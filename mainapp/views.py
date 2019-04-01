from django.shortcuts import render
from .models import Product


def main(request):
    return render(request, 'mainapp/index.html', context={'title': 'interior'})


def products(request):
    # product_list = Product.objects.all()
    return render(request, 'mainapp/products.html', context={'title': 'products'})
                                                             # 'products': product_list})


def contacts(request):
    return render(request, 'mainapp/contacts.html', context={'title': 'contacts'})


def product(request):
    return render(request, 'mainapp/product.html', context={'title': 'product'})
