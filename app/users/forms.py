

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'phone', 'email')

        # help_texts = {
        #     'username': _('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        #     'email': _('Required. Please use a valid email address'),
        #     'password1': _('Your password must contain at least 8 characters.'),
        #     'password2': _('Enter the same password as before, for verification.')
        # }

    email = forms.EmailField()
    phone = forms.CharField(required=False,)


class CustomForm(forms.Form):

    username = forms.CharField(label='Username', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


# 登录注册表单
class TestLogin(forms.Form):

    username = forms.CharField(max_length=30, label='用户名', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=30, label='密码', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        # 这里可以添加验证逻辑
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        # 这里可以添加验证逻辑
        return password


# 注册form表单

class TestRegister(forms.ModelForm):
    username = forms.CharField(
        max_length=15,
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入用户名',
            'max_length': '用户名不能超过15个字符'
        }
    )
    password = forms.CharField(
        max_length=30,
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入密码',
            'min_length': '密码必须至少包含8个字符',
            'invalid': '密码须包含大小写字母和数字'
        }
    )
    email = forms.EmailField()
    phone_number = forms.CharField(
        max_length=11,
        label='手机号',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入手机号',
            'invalid': '请输入11位手机号格式'
        }
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password',  'email', 'phone_number')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 15:
            print('用户名字数不对')
            raise forms.ValidationError('用户名不能超过15个字符')
        if CustomUser.objects.filter(username=username).exists():
            print('重复用户')
            raise forms.ValidationError('该用户名已被占用')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            print('密码位数不够')
            raise forms.ValidationError('密码必须至少包含 8 个字符')
        if not re.search('[a-z]+', password) or not re.search('[A-Z]+', password) or not re.search('[0-9]+', password):
            print('密码格式不对')
            raise forms.ValidationError('密码必须包含大小写字母和数字')
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile('1[3-9][0-9]{9}')
        if not pattern.match(phone_number):
            print('手机号格式不对')
            raise forms.ValidationError('手机号格式错误，请输入11位手机号')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            print('手机号已经被占用')
            raise forms.ValidationError('该手机号已被占用')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            print('邮箱已经被占用')
            raise forms.ValidationError('该邮箱已被占用')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# 忘记密码


class ForgetPassword(forms.Form):

    phone_number = forms.CharField(
        max_length=11,
        label='手机号',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入手机号',
            'invalid': '请输入11位手机号格式'
        }
    )
    code = forms.CharField(max_length=4, label='验证码', required=False)

    def clean_phone_number(self):

        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile('1[3-9][0-9]{9}')
        if not pattern.match(phone_number):
            print('手机号格式不对')
            raise forms.ValidationError('手机号格式错误，请输入11位手机号')

        return phone_number

# 重置密码


class ResetPasswordForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label='手机号',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入手机号',
            'invalid': '请输入11位手机号格式'
        }
    )
    password = forms.CharField(
        max_length=30,
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请输入密码',
            'min_length': '密码必须至少包含8个字符',
            'invalid': '密码须包含大小写字母和数字'
        }
    )

    repassword = forms.CharField(
        max_length=30,
        label='校验密码',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        error_messages={
            'required': '请再次输入密码',
            'min_length': '密码必须至少包含8个字符',
            'invalid': '密码须包含大小写字母和数字'
        }
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            print('密码位数不够')
            raise forms.ValidationError('密码必须至少包含 8 个字符')
        if not re.search('[a-z]+', password) or not re.search('[A-Z]+', password) or not re.search('[0-9]+', password):
            print('密码格式不对')
            raise forms.ValidationError('密码必须包含大小写字母和数字')
        return password

    def clean_phone_number(self):

        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile('1[3-9][0-9]{9}')
        if not pattern.match(phone_number):
            print('手机号格式不对')
            raise forms.ValidationError('手机号格式错误，请输入11位手机号')

        return phone_number

