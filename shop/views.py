from django.shortcuts import render
from .models import Category, Product, Service


# Create your views here.
def all_items(request):
    items = Product.objects.filter(available=True)
    services = Service.objects.filter(available=True)
    context = {
        'items': items,
        'services': services,
    }
    return render(request, "shop/index.html", context=context)


def category(request, slug):
    current = Category.objects.get(slug=slug)
    context = {
        'answer': current.name
    }
    return render(request, "shop/index.html", context=context)


def product(request, item):
    item = Product.objects.get(slug=item)

    context = {
        'item': item,
    }
    return render(request, "shop/product.html", context=context)

