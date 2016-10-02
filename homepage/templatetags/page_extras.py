from django import template

register = template.Library()


@register.inclusion_tag('homepage/menu.html')
def show_menu(path):
    from homepage.models import Page
    menu_pages = Page.objects.filter(menu=True).order_by('-published')
    context = {
        'path': path,
        'menu_pages': menu_pages,
    }
    return context


@register.inclusion_tag('homepage/top.html')
def show_top():
    from homepage.models import MainSetting
    firm_settings = MainSetting.objects.get(active=True)
    context = {
        'firm_settings': firm_settings,
    }
    return context
