from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name


class Dish(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_dish'
        verbose_name = '菜品名'
        verbose_name_plural = verbose_name


class FoodCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_food_category'
        verbose_name = '菜单分类'
        verbose_name_plural = verbose_name


class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food/')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_food'
        verbose_name = '菜品详情'
        verbose_name_plural = verbose_name
