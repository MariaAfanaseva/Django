from django import template
register = template.Library()


@register.filter
def basket_total_cost(basket):
    if len(basket) == 0:
        return 0
    else:
        # items = user.basket.select_related('product').all()
        total_cost = sum(list(map(lambda x: x.product.price*x.quantity, basket)))
        return total_cost


@register.filter
def basket_total_quantity(basket):
    if len(basket) == 0:
        return 0
    else:
        # items = user.basket.all()
        total_quantity = sum(list(map(lambda x: x.quantity, basket)))
        return total_quantity

