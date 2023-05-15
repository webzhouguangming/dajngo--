from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Order


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # order_number = self.kwargs.get('order_number')
        # order = get_object_or_404(Order, order_number=order_number)
        # context['order'] = order  # 将每个订单明细字段添加到上下文中，以便在模板中使用。
        return context


class Pay(View):

    def get(self, request):
        return render(request, template_name='order/pay_success.html')

