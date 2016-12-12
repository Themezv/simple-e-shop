from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect


from orders.forms import OrderForm
from shop.models import Product
from orders.models import Order, OrderedItem
# Create your views here.

@csrf_protect
def order_list(request):
    if not request.user.is_superuser or not request.user.is_staff:
        raise Http404
    queryset_list = Order.objects.all()

    ##################Search###################

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                            Q(FIO__icontains=query) |
                            Q(adress__icontains=query) |
                            Q(email__icontains=query)).distinct()


    #################Paginator#################

    paginator = Paginator(queryset_list, 10)
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
        'obj_list': queryset,#object_list v html
        'page_request_var': page_request_var, #v url num page
    }

    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise Http404

    instance = get_object_or_404(Order, id=order_id)

    ordered_product = instance.items.filter(service=None)
    ordered_service = instance.items.filter(product=None)

    context = {
        'instance': instance,
        'ordered_product':ordered_product,
        'ordered_service':ordered_service,
    }
    return render(request, "orders/order_detail.html", context)


def order_delete(request, order_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Order, id=order_id)

    #FOR ADDING: DELETE linked OrderedItem
    
    instance.delete()

    return redirect("order_list")


def order_create(request):
    count = request.POST.get('count')
    id_item = request.POST.get('id_service')
    try:
        instance = Service.objects.get(id=id_item)
        ordered_item = OrderedItem(service=instance, count=count)
    except:
        instance = Product.objects.get(id=id_item)
        ordered_item = OrderedItem.objects.create(product=instance, count=count)

    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        ordered_item.save()
        order.save()
        order.items.add(ordered_item)
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form':form,
        'instance':instance,
        'count':count,
    }

    return render(request, "orders/order_create.html", context)

