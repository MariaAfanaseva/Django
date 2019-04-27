from django.shortcuts import render
from .models import ProductCategory


def main(request):
    return render(request, 'mainapp/index.html', context={'user':request.user,'title': 'interior'})


def products(request, pk=None):
    products_category = ProductCategory.objects.all()
    return render(request, 'mainapp/products.html',
                  context={'title': 'products','categories': products_category})


def contacts(request):
    return render(request, 'mainapp/contacts.html', context={'title': 'contacts'})


def product(request):
    return render(request, 'mainapp/product.html', context={'title': 'product'})
