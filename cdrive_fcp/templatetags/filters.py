from django import template
from cdrive_fcp.utils.utils import HelperUtils
from cdrive_fcp.utils.const import RewardsConst
from decimal import Decimal

from core.models import CartGamePurchase

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='formfieldname')
def formfieldname(value):
    return value.replace('_', ' ').capitalize()

@register.filter(name='toint')
def toint(value):
    return int(value)

@register.filter(name='groupin')
def groupin(value, num):
    return HelperUtils.get_column_groups(value, num_of_cols=num)


@register.filter(name='gamerewards')
def gamerewards(cart, game_id):
    return CartGamePurchase.objects.get(cart=cart, game_id=game_id).rewards

@register.filter(name='discount')
def discount(price, rewards):
	return HelperUtils.get_discount_str(price, rewards)

@register.filter(name='subtotal')
def subtotal(price, rewards):
	return HelperUtils.get_subtotal_str(price, rewards)

