
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from menus.models import Food, FoodCategory
from .forms import CustomUserCreationForm, CustomForm
from orders.models import Order


def home_view(request):
    return render(request, 'index.html')


class FoodListView(ListView):
    model = Food
    template_name = 'food/list.html'
    context_object_name = 'food_list'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Food.objects.filter(name__icontains=query)
        else:
            return Food.objects.all()


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food/detail.html'


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return redirect('users:login')
        else:
            messages.error(request, '注册失败！请检查输入内容。')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = CustomUser.objects.filter(username=username).first()
            if user:
                if user.check_password(password):
                    user.is_active = 1
                    user.save()
                    login(request, user)
                    return redirect('menus:list')


                else:
                    messages.error(request, '无效的用户名或密码，请重试！')
            else:
                messages.error(request, '不存在该用户，请重试！')
    else:
        form = CustomForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('users:home')


class UserProfileView(View):

    def get(self, request):
        user = CustomUser.objects.filter(is_active=1).first()
        orders = Order.objects.all()

        return render(request, template_name='users/user_center.html', context={'user': user, 'orders': orders})




