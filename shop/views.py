from django.shortcuts import render
from .models import Category, Product


# Create your views here.
def in_work(request):
    context = {
        'answer': "app in dev",
    }
    return render(request, "shop/index.html", context=context)


def category(request, slug):
    current = Category.objects.get(slug=slug)
    context = {
        'answer': current.name
    }
    return render(request, "shop/index.html", context=context)


def product(request, cat, item):
    current_category = Category.objects.get(slug=cat)
    items = Product.objects.filter(category=current_category)
    current_item = items.get(name=item)
    context = {
        'cat': current_category.name,
        'items': items,
        'item': current_item,
    }
    return render(request, "shop/product.html", context=context)

