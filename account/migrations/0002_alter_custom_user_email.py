# Generated by Django 4.2.5 on 2023-09-08 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='email',
            field=models.EmailField(default='', max_length=255, verbose_name='email adress'),
        ),
    ]
