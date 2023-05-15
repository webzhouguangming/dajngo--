
from django.shortcuts import get_object_or_404, redirect, render
from .models import CartItem
from .forms import AddToCartForm
from users.models import CustomUser
from orders.forms import OrderForm
from django.utils.crypto import get_random_string
from orders.models import Order


def cart_view(request):
    login_user = CustomUser.objects.get(is_active=1)
    cart_items = CartItem.objects.filter(user=login_user).select_related('menu_item')
    total_price = sum([item.total_price for item in cart_items])

    # 新加订单代码
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_number = get_random_string(length=8)  # 生成唯一订单编号
            table_number = form.cleaned_data['table_number']
            order = Order.objects.create(
                order_number=order_number,
                total_price=total_price,
                user=login_user,
            )
            # order.cart_items.set(cart_items)
            order.save()
            # 清空购物车
            cart_list = CartItem.objects.filter(user=login_user)
            for item in cart_list:
                item.delete()

            return redirect('orders:detail', order.order_number)
    else:
        form = OrderForm()

    return render(request, 'cart/cart1.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form})



