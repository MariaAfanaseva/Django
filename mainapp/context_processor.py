def basket(request):
    # print(f'context processor basket works')
    basket = []
    if request.user.is_authenticated:
       basket = request.user.basket.all().select_related('product__category')
    return {
       'basket': basket,
    }
