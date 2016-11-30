from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from orders.forms import OrderForm

from .models import Category, Product, Service


# Create your views here.
@csrf_protect
def product_list(request):
    queryset_list = Product.objects.all()
    

    user = request.user
    categories = Category.objects.all()[:10]

    ##################Search###################

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(name__icontains=query)).distinct()


    #################Paginator#################

    paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
    page_request_var='page' #url name 'page'=1,2,3,4...
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'products': queryset,#object_list v html
        'page_request_var': page_request_var, #v url num page
        'categories':categories,
        'user': user,
    }

    return render(request, "shop/product_list.html", context)



@csrf_protect
def product_categoried_list(request, category_slug):
    queryset_list = Product.objects.filter(category__slug=category_slug)
    

    user = request.user
    category_url = category_slug
    another_categories = Category.objects.all()[:10]

    ##################Search###################

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(name__icontains=query)).distinct()


    #################Paginator#################

    paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
    page_request_var='page' #url name 'page'=1,2,3,4...
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'products': queryset,#object_list v html
        'page_request_var': page_request_var, #v url num page
        'category_slug':category_slug,
        'another_categories':another_categories,
        'user': user,
    }

    return render(request, "shop/product_list.html", context)


def product_detail(request, product_slug):
    item = get_object_or_404(Product, slug=product_slug)

    related_items = Product.objects.filter(relation=item).distinct()

    context = {
        'item': item,
        'related_items':related_items,
    }

    return render(request, "shop/product_detail.html", context=context)


def service_list(request):
    queryset_list = Service.objects.filter(available=True)


    ##################Search###################

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(name__icontains=query)).distinct()


    #################Paginator#################

    paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
    page_request_var='page' #url name 'page'=1,2,3,4...
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'services': queryset,
        'page_request_var': page_request_var,
    }

    return render(request, "shop/service_list.html", context=context)


def category_list(request):
    queryset_list = Category.objects.all()

    ##################Search###################

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(name__icontains=query)).distinct()


    #################Paginator#################

    paginator = Paginator(queryset_list, 5) #Show 5 contacts per page
    page_request_var='page' #url name 'page'=1,2,3,4...
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        'categories': queryset,
        'page_request_var': page_request_var,
    }

    return render(request, "shop/category_list.html", context=context)

 

def service_detail(request, service_slug):
    item = get_object_or_404(Service, slug=service_slug)


    related_services = Service.objects.filter(relation=item).distinct()

    related_productes = Product.objects.filter(relation=item).distinct()

    context = {
        'item': item,
        'related_services':related_services,
        'related_productes':related_productes,
    }

    return render(request, "shop/service_detail.html", context=context)
 

