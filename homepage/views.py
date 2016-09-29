from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect

#import forms
from .forms import PageForm


from .models import Page, MainSetting


# @csrf_protect
def index(request):
    user = request.user
    firm_settings = MainSetting.objects.get(active=True)
    menu_pages = Page.objects.filter(menu=True).order_by('-published')  # pages to nav-menu
    tiles_pages = Page.objects.filter(tile=True).order_by('-published')  # pages to tales


    #Search

    query = request.GET.get("q")
    if query:
        tiles_pages = tiles_pages.filter(
                Q(title__icontains=query) |     
                Q(content__icontains=query)
                #Q(user__first_name__icontains=query) |
                #Q(user__last_name__icontains=query) 
                ).distinct()


    #Paginator

    paginator = Paginator(tiles_pages, 1)
    page_request_var='page'#url name 'page'=1,2,3,4...
    page = request.GET.get(page_request_var)

    try:
        tiles_pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tiles_pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tiles_pages = paginator.page(paginator.num_pages)



    context = {
        'menu_pages': menu_pages,
        'firm_settings': firm_settings,
        'tiles_pages': tiles_pages,
        'user': user,
        'page_request_var':page_request_var,
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

# @csrf_protect
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

