# Generated by Django 3.1.6 on 2021-03-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=models.ImageField(default='background.jpg', upload_to='backgrounds'),
        ),
    ]
