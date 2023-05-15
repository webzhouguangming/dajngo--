from django.db import models

# Create your models here.
from users.models import CustomUser
from django.conf import settings


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, primary_key=True)  # 订单编号
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 总价格
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 下单用户

    def __str__(self):
        return self.order_number

