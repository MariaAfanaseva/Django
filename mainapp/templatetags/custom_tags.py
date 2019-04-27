from django import template

register = template.Library()


@register.filter
def basket_total_cost(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        total_cost = sum(list(map(lambda x: x.product.price*x.quantity, items)))
        return total_cost


@register.filter
def basket_total_quantity(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.all()
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return total_quantity

