
from .models import CartItem

from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    table_num = forms.CharField(max_length=20)


