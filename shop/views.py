from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from blog.views import CategoryListView
from .models import Category, Product, ProductType
from .forms import ProductForm


class ProductListView(ListView):
    template_name = "shop/product_list.html"
    model = Product

    paginate_by = 10

    def get_queryset(self):
        queryset_list = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            return queryset_list.filter(Q(title__icontains=query)).distinct()
        else:
            return queryset_list


class ItemListView(ProductListView):
    context_object_name = 'products'

    def get_queryset(self):
        """ Нужно сделать создав метод для Queryser """
        queryset_list = super(ItemListView, self).get_queryset()
        queryset_list = queryset_list.filter(product_type__title="Item")
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:10]
        return context


class ServiceListView(ProductListView):
    template_name = "shop/service_list.html"
    context_object_name = 'services'

    def get_queryset(self):
        """ Нужно сделать создав метод для Queryser """
        queryset_list = super(ServiceListView, self).get_queryset()
        queryset_list = Product.objects.filter(product_type__title="Service")
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:10]
        return context


class CategoryShopListView(CategoryListView):
    template_name = "shop/category_list.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryShopListView, self).get_context_data(**kwargs)
        return context


class ItemCategoriedListView(ItemListView):
    def get_queryset(self):
        queryset_list = super(ItemCategoriedListView, self).get_queryset()
        return queryset_list.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super(ItemCategoriedListView, self).get_context_data(**kwargs)
        context['another_categories'] = Category.objects.all()[:10]
        context['category_slug'] = self.kwargs['category_slug']
        return context

    def get(self, request, *args, **kwargs):
        # context = super(ItemCategoriedListView, self).get_context_data(**kwargs)
        return super(ItemCategoriedListView, self).get(self.request, *args, **kwargs)


class ProductDetalilView(DetailView):
    model = Product
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ProductDetalilView, self).get_context_data(**kwargs)
        item = context['object']
        related_items = Product.objects.items().filter(relation=item).distinct().exclude(id=item.id)
        related_services = Product.objects.services().filter(relation=item).distinct().exclude(id=item.id)
        context['related_items'] = related_items[:4]
        context['related_services'] = related_services[:4]
        return context


class ItemDetailView(ProductDetalilView):
    template_name = "shop/product_detail.html"


class ServiceDetailView(ProductDetalilView):
    template_name = "shop/service_detail.html"


@method_decorator(login_required(), name="dispatch")
class ProductCreateView(CreateView):
    template_name = "shop/product_create.html"
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

