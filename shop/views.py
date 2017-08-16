from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from blog.views import CategoryListView
from extuser.forms import ExtUserForm
from .models import Category, Product, ProductGroup, Manufacturer, Service
from .forms import ProductForm


class ProductListView(ListView):
    template_name = "shop/product_list.html"
    model = Product
    paginate_by = 10


class FilteredProductListView(ListView):
    model = Product
    template_name = "shop/product_list_ajax.html"

    def get_queryset(self):
        category_slug_list = self.request.GET.getlist("category")
        manufacturer_slug = self.request.GET.getlist("manufacturer")
        group_slug = self.request.GET.get("group")

        queryset_list = super(FilteredProductListView, self).get_queryset().filter(group__slug=group_slug)

        if category_slug_list:
            queryset_list = queryset_list.filter(category__slug__in=category_slug_list)

        if manufacturer_slug:
            queryset_list = queryset_list.filter(manufacturer__slug__in=manufacturer_slug)

        if queryset_list.exists():
            return queryset_list
        else:
            return HttpResponse("<h2>Нет таких товаров</h2>")


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'item'
    template_name = "shop/product_detail.html"


    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = ExtUserForm
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetalilView, self).get_context_data(**kwargs)
    #     item = context['object']
    #     related_items = Product.objects.items().filter(relation=item).distinct().exclude(id=item.id)
    #     related_services = Product.objects.services().filter(relation=item).distinct().exclude(id=item.id)
    #     context['related_items'] = related_items[:4]
    #     context['related_services'] = related_services[:4]
    #     return context


class ServiceListView(ListView):
    template_name = "shop/service_list.html"
    context_object_name = 'services'
    model = Service


class ServiceDetailView(DetailView):
    template_name = "shop/service_detail.html"
    model = Service
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['form'] = ExtUserForm
        return context


@method_decorator(login_required(), name="dispatch")
class ProductCreateView(CreateView):
    template_name = "shop/product_create.html"
    model = Product
    form_class = ProductForm
    context_object_name = 'product'


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'shop/manufacturer_detail.html'
