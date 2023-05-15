from django.db import models
from menus.models import Food
from users.models import CustomUser


class CartItem(models.Model):
    menu_item = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    table_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.menu_item} x {self.quantity} ({self.user.username})"

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

    class Meta:
        db_table = 't_cart_item'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
