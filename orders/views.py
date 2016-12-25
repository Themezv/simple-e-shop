from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, DeleteView, TemplateView
from django.utils.decorators import method_decorator




from orders.forms import OrderForm
from shop.models import Product
from orders.models import Order, OrderedItem
# Create your views here.

@method_decorator(login_required(), name="dispatch")
class OrderListView(ListView):
    template_name = "orders/order_list.html"
    model = Order
    context_object_name = 'obj_list'

    paginate_by = 10

    def get_queryset(self):
        queryset_list = super(OrderListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            return queryset_list.filter(
                            Q(FIO__icontains=query) |
                            Q(adress__icontains=query) |
                            Q(email__icontains=query)).distinct()
        else:
            return queryset_list


@method_decorator(login_required(), name="dispatch")
class OrderDetailView(DetailView): 
    template_name = "orders/order_detail.html"
    model = Order
    context_object_name = 'instance'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        instance = context['instance']
        context['ordered_products'] = instance.items.all()
        return context

#Не сделанно
@method_decorator(login_required(), name="dispatch")
class OrdereDeleteView(DeleteView):
    template_name = "orders/order_create.html"
    model = Order
    form_class = OrderForm


class OrderCreateView(CreateView):
    template_name = "orders/order_create.html"
    Model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        count = self.request.POST.get('count')
        id_item = self.request.POST.get('id_product')
        product = Product.objects.get(id=id_item)
        ordered_item = OrderedItem(product=product, count=count)
        context['ordered_item'] = ordered_item
        context['count'] = count
        return context

    def form_valid(self, form):
        ordered_item = self.get_context_data()['ordered_item']
        ordered_item.save()
        self.object = form.save(commit=False)
        self.object.save()
        self.object.items.add(ordered_item)
        return self.get_success_url()

    def get_success_url(self):
        #Нужно переделать
        return HttpResponseRedirect('/')