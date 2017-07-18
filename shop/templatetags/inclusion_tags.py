from django import template

from shop.models import ProductGroup

register = template.Library()


@register.inclusion_tag('shop/filter_panel.html')
def show_filter_panel():
    context = {
        'product_groups': ProductGroup.objects.all()
    }
    return context
