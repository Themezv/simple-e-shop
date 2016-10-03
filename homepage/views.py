from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Page, MainSetting


@csrf_protect
def index(request):
    user = request.user
    menu_pages = Page.objects.filter(menu=True).order_by('-published')  # pages to nav-menu
    tiles_pages = Page.objects.filter(tile=True).order_by('-published')  # pages to tales

    context = {
        'menu_pages': menu_pages,
        'tiles_pages': tiles_pages,
        'user': user,
        }
    return render(request, 'homepage/index.html', context)


@csrf_protect
def page_detail(request, slug='main'):
    page = get_object_or_404(Page, slug=slug)
    user = request.user
    firm_settings = MainSetting.objects.get(active=True)
    menu_pages = Page.objects.filter(menu=True)  # pages to nav-menu
    context = {
        'page': page,
        'menu_pages': menu_pages,
        'firm_settings': firm_settings,
        'user': user,
        }
    return render(request, 'homepage/pages.html', context)

