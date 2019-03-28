
from django.shortcuts import render

# Create your views here.


def main(request):
    return render(request, 'mainapp/index.html', context={'title': 'interior'})


def products(request):
    return render(request, 'mainapp/products.html', context={'title': 'products'})


def contacts(request):
    return render(request, 'mainapp/contacts.html', context={'title': 'contacts'})


def product(request):
    return render(request, 'mainapp/product.html', context={'title': 'product'})
