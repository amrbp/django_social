# Generated by Django 3.1.6 on 2021-03-19 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20210319_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
