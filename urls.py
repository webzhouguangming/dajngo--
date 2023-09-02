"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from djangoProject import settings, static

# from djangoProject.app.home.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'ckeditor/', include('ckeditor_uploader.urls')),
    re_path('^', include(('home.urls', 'home'), namespace='home')),
    re_path('^', include(('users.urls', 'users'), namespace='users')),
    re_path('^', include(('article.urls', 'article'), namespace='articles')),
    re_path('^', include(('message.urls', 'message'), namespace='messages')),
    re_path(r'^search/', include('haystack.urls')),


]
