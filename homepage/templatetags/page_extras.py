from django import template

register = template.Library()


@register.inclusion_tag('homepage/menu.html')
def show_menu():
    from homepage.models import Page
    menu_pages = Page.objects.filter(menu=True).order_by('-published')
    context = {
        'menu_pages': menu_pages,
    }
    return context
