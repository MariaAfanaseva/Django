from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from basketapp.models import Basket
from mainapp.models import Product
from django.urls import reverse


@login_required
def basket(request):
    title = 'Basket'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    context = {'basket_items': basket_items,
               'title': title,
               }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = Basket.objects.filter(user=request.user, pk=pk).first()

    if basket:
        if basket_record.quantity > 1:
            basket_record.quantity -= 1
            basket_record.save()
        else: basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk):
    if request.is_ajax():
        quantity = int(request.GET.get('quantity'))
        basket_record = get_object_or_404(Basket, pk=pk)

        if quantity > 0:
            basket_record.quantity = quantity
            basket_record.save()
        else:
            basket_record.delete()

        # return HttpResponse('ok')

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
        context = {'basket_items': basket_items, }
        result = render_to_string('basketapp/includes/inc_basket_total.html', context)
        return JsonResponse({'result': result})
