# Generated by Django 5.0.6 on 2024-05-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appname', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='logo')),
                ('carousel1', models.ImageField(upload_to='carousel')),
                ('carousel2', models.ImageField(upload_to='carousel')),
                ('carousel3', models.ImageField(upload_to='carousel')),
                ('banner', models.ImageField(upload_to='banner')),
                ('copyright', models.IntegerField()),
            ],
        ),
    ]
