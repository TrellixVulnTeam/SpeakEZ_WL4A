# Generated by Django 2.2.1 on 2019-05-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
