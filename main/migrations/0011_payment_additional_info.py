# Generated by Django 5.0.6 on 2024-05-21 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='additional_info',
            field=models.TextField(default='a'),
        ),
    ]
