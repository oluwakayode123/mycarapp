# Generated by Django 5.0.6 on 2024-05-17 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_color_alter_product_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='carousel4',
            field=models.ImageField(default='.jpg', upload_to='carousel4'),
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='carousel1',
            field=models.ImageField(upload_to='carousel1'),
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='carousel2',
            field=models.ImageField(upload_to='carousel2'),
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='carousel3',
            field=models.ImageField(upload_to='carousel3'),
        ),
    ]