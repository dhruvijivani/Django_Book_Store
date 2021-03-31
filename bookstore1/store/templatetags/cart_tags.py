from django import template
from math import floor

register = template.Library()

@register.simple_tag
def multiply(a , b ):
    return a*b

@register.filter
def cal_total_payable_amount(cart):
    total=0
    for c in cart:
        b=c.get('book')
        price=c.get('book').price
        total_of_single_book=price * c.get('quantity')
        total= total + total_of_single_book
    return total

@register.filter(name='is_in_cart')
def is_in_cart(book , cart):
    keys = [d['book'] for d in cart]
    for id in keys:
        if book.id == id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(book  , cart):
    keys = [d['book'] for d in cart]
    quantity = [d['quantity'] for d in cart]
    for i in range(len(keys)):
        if book.id == keys[i]:
            return quantity[i]
    return 0