from django import template
from kitty.models import *
from django.db import models

register = template.Library()

main_menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]

@register.inclusion_tag('kitty/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('kitty/menu.html')
def menu():
    menu = main_menu
    return {'menu': menu}
