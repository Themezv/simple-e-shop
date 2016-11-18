from django import template

register = template.Library()


@register.inclusion_tag('homepage/menu.html')
def show_menu(path):
    context = {
        'path': path,
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
