# Generated by Django 2.2.2 on 2019-06-06 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20190605_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
    ]
