# Generated by Django 3.1.6 on 2021-03-12 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20210312_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
    ]
