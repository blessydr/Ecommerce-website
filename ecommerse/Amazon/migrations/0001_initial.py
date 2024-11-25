# Generated by Django 4.2.16 on 2024-11-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Mens Wear', "Men's Wear"), ('Womens Wear', "Women's Wear"), ('Kids Wear', "Kids' Wear"), ('Accessories', 'Accessories'), ('Footwear', 'Footwear'), ('Sportswear', 'Sportswear'), ('Home Decor', 'Home Decor'), ('Electronics', 'Electronics')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
                ('sizes', models.CharField(max_length=50)),
                ('colors', models.CharField(max_length=50)),
                ('availability', models.BooleanField(default=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('discount', models.CharField(blank=True, max_length=20, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('star', models.IntegerField(default=0)),
            ],
        ),
    ]
