
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from menus.models import Food, FoodCategory
from .forms import CustomUserCreationForm, CustomForm, TestLogin, TestRegister, ForgetPassword, ResetPasswordForm
from orders.models import Order
import random
import threading
import django_redis
from django_redis import client
from djangoProject.utils.sms import send_sms_code

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
        form = TestRegister(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return redirect('users:login')
        else:
            messages.error(request, '注册失败！请检查输入内容。')
    else:
        form = TestRegister()

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
                    print(request.user)
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


# 登录视图
def login_view2(request):
    if request.method == 'POST':
        form = TestLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username:
                user = CustomUser.objects.filter(username=username).first()
                if user.check_password(password):
                    # user = authenticate(request, username=username, password=password)
                    # if user is not None:
                    login(request, user)
                    print('登陆成功')
                    messages.success(request, '登录成功')
                    return redirect('home:home')
                else:
                    print('登录失败')
                    messages.error(request, '用户名或密码错误')
    else:
        form = TestLogin()

    context = {'form': form}

    return render(request, 'test_files/test_login.html', context)


# 注册视图
def signup_view2(request):
    if request.method == 'POST':
        form = TestRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, '注册成功')
            return JsonResponse({'success': True, 'message': '注册成功，即将跳转到登录页面'})
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.append(f"{field.capitalize()}: {', '.join(errors)}")
            print(error_messages)
            return JsonResponse({'success': False, 'errors': error_messages})
    else:
        form = TestRegister()

    return render(request, 'test_files/test_register.html', {'form': form})

# 发送验证码


def send_code(request):
    if request.method == 'POST':
        form = ForgetPassword(request.POST)
        if not form.is_valid():
            print('无效的表单数据')
            return JsonResponse({
                'status': 'error',
                'message': '参数错误'
            })
        phone_number = form.cleaned_data['phone_number']
        smscode = random.randint(1000, 9999)  # 生成验证码
        print(smscode)
        # 发送验证码的异步处理，防止阻塞 Web 服务器的请求处理
        thr = threading.Thread(target=send_code_async, args=(phone_number, smscode))
        thr.start()
        # 将验证码存储到redis中，60秒后过期
        redis_conn = django_redis.get_redis_connection('verify_code')
        generate_sms = str(smscode)
        redis_conn.setex('sms_%s' % phone_number, 60, generate_sms)
        return JsonResponse({
            'status': 'success',
            'message': '发送成功'
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': '请求方法不支持'
        })


def send_code_async(phone_number, smscode):
    result = send_sms_code(smscode, phone_number)  # 调用互亿无线短信 API 发送验证码
    print('测试send_code_async接口')  # 打印返回结果，用于调试



# 忘记密码页面


class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPassword()
        return render(request, 'test_files/test_forgetpassword.html', {'form': form})

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        code = request.POST.get('code')
        print('==========当前测试内容==============')
        print(code)
        print(phone_number)
        print('===========测试完毕=================')
        if not phone_number or not code:
            return JsonResponse({
                'status': 'error',
                'message': '参数错误'
            })
        # 从redis中获取验证码
        redis_conn = django_redis.get_redis_connection('verify_code')
        cached_code = redis_conn.get('sms_%s'%phone_number)
        if not cached_code:

            return JsonResponse({
                'status': 'error',
                'message': 'The verification code has expired Please obtain it again'
            })

        # if code != cached_code:
        #     return JsonResponse({
        #         'status': 'error',
        #         'message': 'verify error'
        #     })

        return JsonResponse({
            'status': 'success',
            'message': 'verify success'
        })

# 重置密码


class ResetPassword(View):
    def get(self, request):

        form = ResetPasswordForm()
        return render(request, 'test_files/test_setpassword.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm()
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(password)
        repassword = request.POST.get('repassword')
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        print(user)
        if user:
            if password == repassword:
                user.password = user.set_password(password)
                return JsonResponse({'success': True, 'message': '重置密码成功，即将跳转到登录页面'})

            else:
                error_messages = []
                for field, errors in form.errors.items():
                    error_messages.append(f"{field.capitalize()}: {', '.join(errors)}")
                print(error_messages)
                return JsonResponse({'success': False, 'errors': error_messages})


        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.append(f"{field.capitalize()}: {', '.join(errors)}")
            print(error_messages)
            return JsonResponse({'success': False, 'errors': error_messages})


