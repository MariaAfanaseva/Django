from django import template

register = template.Library()


@register.filter
def basket_total_cost(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        totalcost = sum(list(map(lambda x: x.product.price*x.quantity, items)))
        return totalcost


@register.filter
def basket_total_quantity(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.all()
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

