from django import template

register = template.Library()


@register.inclusion_tag('homepage/menu.html', takes_context=True)
def show_menu(context, path):
    request = context['request']
    user = request.user
    context = {
        'path': path,
        'user': user,
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
