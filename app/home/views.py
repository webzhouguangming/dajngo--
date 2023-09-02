
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class Index(View):

    def get(self, request):
        print(request.user)
        return render(request, template_name="index.html")


class Test(View):

    def get(self, request):
        return render(request, template_name='test_files/test_model.html')

    def post(self, request):
        return JsonResponse(data={'message': '测试成功'})


class AboutWebsiteView(View):

    def get(self, request):
        return render(request, template_name='about_website/about_web.html')

    def post(self, request):
        pass
