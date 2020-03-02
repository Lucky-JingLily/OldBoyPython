from django import template
from django.utils.safestring import mark_safe

register = template.Library()   #register的名字是固定的,不可改变

# simple_tag可以多个参数，filter最多有2个参数
# 但是{% if %}后面只能是filter

@register.simple_tag
def my_add100_tag(value):
    return value + 100

@register.filter
def my_add100_filter(value1, value2):
    return value1 + 100 + value2