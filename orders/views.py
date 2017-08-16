import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from orders.forms import OrderForm
from orders.models import OrderProduct, OrderService
from extuser.forms import ExtUserForm
from shop.models import Product, Service


class OrdersListView(TemplateView):
    template_name = 'orders/order_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersListView, self).get_context_data()
        product_orders = OrderProduct.objects.all().order_by('-date')
        service_orders = OrderService.objects.all().order_by('-date')
        context['product_orders'] = product_orders
        context['service_orders'] = service_orders
        return context


class OrderCreate(FormView):
    model = None
    item_model = None

    def get(self, request, *args, **kwargs):
        raise Http404

    @staticmethod
    def user_form_init(user_data):
        user_initial = {}
        for foo in user_data:
            user_initial[str(foo["name"])] = foo["value"]

        return ExtUserForm(user_initial)

    @staticmethod
    def order_form_init(order_data):
        order_initial = {
            'item_id': order_data['item_id'],
            'count': getattr(order_data, 'count', None)
        }

        return OrderForm(order_initial)

    def forms_valid(self, order_form, user_form):
        pass

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body.decode("utf-8"))
        self.data = request_data

        if request_data['user']:
            user_form = self.user_form_init(request_data['user'])
        else:
            raise Http404

        if request_data['order']:
            order_form = self.order_form_init(request_data['order'])
        else:
            raise Http404

        if user_form.is_valid() and order_form.is_valid():
            self.forms_valid(order_form, user_form)
            return HttpResponse("OK", status=204)
        else:
            print("Invalid")
            raise Http404


class ProductOrderCreate(OrderCreate):
    model = OrderProduct
    item_model = Product

    def forms_valid(self, order_form, user_form):
        user = user_form.save()
        product = get_object_or_404(self.item_model, id=self.data['order']['item_id'])

        order = self.model.objects.create(
            user=user,
            product=product,
            count=self.data['order']['count']
        )


class ServiceOrderCreate(OrderCreate):
    model = OrderService
    item_model = Service

    def forms_valid(self, order_form, user_form):
        user = user_form.save()
        service = get_object_or_404(self.item_model, id=self.data['order']['item_id'])

        order = self.model.objects.create(
            user=user,
            service=service,
        )
