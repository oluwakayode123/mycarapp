# Generated by Django 5.0.6 on 2024-05-17 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_appinfo_carousel4_alter_appinfo_carousel1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='carousel4',
            field=models.ImageField(upload_to='carousel4'),
        ),
    ]
