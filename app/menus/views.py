
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Food, FoodCategory
from .forms import FoodSearchForm
from carts.forms import AddToCartForm
from carts.models import CartItem
from users.models import CustomUser


class FoodListView(ListView):
    model = Food
    template_name = 'food/list.html'
    context_object_name = 'food_list'
    paginate_by = 6

    def get_queryset(self):
        queryset = super(FoodListView, self).get_queryset()
        category_id = self.request.GET.get('category', None)
        name = self.request.GET.get('name', None)

        if category_id:
            queryset = queryset.filter(category=category_id)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(FoodListView, self).get_context_data(**kwargs)
        context['form'] = FoodSearchForm(data=self.request.GET or None)
        return context


def food_detail_view(request, pk):
    food = Food.objects.get(pk=pk)
    form = AddToCartForm(request.POST or None)
    return render(request, 'food/detail.html', {'food': food, 'form': form})


def add_to_cart_view(request, pk):

    item = get_object_or_404(Food, pk=pk)
    form = AddToCartForm(request.POST or None)
    login_user = CustomUser.objects.get(is_active=1)

    if request.method == 'POST' and form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        table_number = form.cleaned_data.get('table_num')

        cart_item, created = CartItem.objects.get_or_create(
            menu_item=item,
            user=login_user,
            defaults={'quantity': quantity, 'table_number': table_number},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('carts:cart')

    return render(request, 'food/add_to_cart.html', {'menu_item': item, 'form': form})


