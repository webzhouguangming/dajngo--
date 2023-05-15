# Generated by Django 4.1.6 on 2023-05-14 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_delete_passwordresettoken'),
        ('menus', '0002_foodcategory_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('table_number', models.CharField(max_length=20)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
                'db_table': 't_cart_item',
            },
        ),
    ]
