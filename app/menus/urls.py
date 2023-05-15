
from django.urls import path

from .views import FoodListView, food_detail_view, add_to_cart_view
from djangoProject import settings
from django.conf.urls.static import static

app_name = 'foods'

urlpatterns = [
    path('menu_index/', FoodListView.as_view(), name='list'),
    path('<int:pk>/', food_detail_view, name='detail'),
    path('<int:pk>/add_to_cart/', add_to_cart_view, name='add_to_cart'),
]

# 为了显示上传的图片，不加的话无法显示
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

