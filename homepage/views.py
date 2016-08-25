from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Page, MainSetting


@csrf_protect
def index(request):
    firm_settings = MainSetting.objects.get(active=True)
    menu_pages = Page.objects.filter(menu=True)  # pages to nav-menu
    tiles_pages = Page.objects.filter(tile=True)  # pages to tales
    context = {
        'menu_pages': menu_pages,
        'firm_settings': firm_settings,
        'tiles_pages': tiles_pages,
        }
    return render(request, 'homepage/index.html', context)


@csrf_protect
def page(request, page_lable='main'):
    cpage = Page.objects.get(lable=page_lable)
    firm_settings = MainSetting.objects.get(active=True)
    pages = Page.objects.all()
    menu_pages = Page.objects.filter(menu=True)  # pages to nav-menu
    context = {
        'cpage': cpage,
        'pages': pages,
        'page_lable': page_lable,
        'menu_pages': menu_pages,
        'firm_settings': firm_settings,
        }
    return render(request, 'homepage/pages.html', context)

