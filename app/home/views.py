
# Create your views here.

from django.shortcuts import render
from django.views import View


class Index(View):

    def get(self, request):
        return render(request, template_name="index.html")


class Test(View):

    def get(self, request):
        return render(request, template_name='test_files/test1.html')