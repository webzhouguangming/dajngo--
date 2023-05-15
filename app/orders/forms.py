from django import forms


class OrderForm(forms.Form):

    table_number = forms.CharField(max_length=20, required=True)
