from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='formfieldname')
def formfieldname(value):
    return value.replace('_', ' ').capitalize()