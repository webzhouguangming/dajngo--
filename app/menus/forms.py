

from django import forms
from .models import FoodCategory, Food


class FoodSearchForm(forms.Form):
    name = forms.CharField(required=False, max_length=50, label='搜索')
    category = forms.ModelChoiceField(queryset=FoodCategory.objects.all(), required=False,label='分类')


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'price', 'description', 'image', 'category']
        labels = {
            'name': '菜品名称',
            'price': '价格',
            'description': '描述',
            'image': '图片',
            'category': '分类',
        }

        widgets = {
            'description': forms.Textarea(),
            'category': forms.Select,
        }
