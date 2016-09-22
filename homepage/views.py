from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect

#import forms
from .forms import PageForm


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


def page_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, "homepage/page_form.html", context)

def page_edit(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Page, slug=slug)
    form = PageForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'instance':instance,
        'form': form
    }
    return render(request, "homepage/page_form.html", context)

def page_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Page, slug=slug)
    instance.delete()
    return redirect("index")   

@csrf_protect
def page_detail(request, slug='main'):
    cpage = get_object_or_404(Page, slug=slug)
    firm_settings = MainSetting.objects.get(active=True)
    pages = Page.objects.all()
    menu_pages = Page.objects.filter(menu=True)  # pages to nav-menu
    context = {
        'cpage': cpage,
        'pages': pages,
        #'page_lable': page_lable,
        'menu_pages': menu_pages,
        'firm_settings': firm_settings,
        }
    return render(request, 'homepage/pages.html', context)

