from django import template
from cdrive_fcp.utils.utils import HelperUtils

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

