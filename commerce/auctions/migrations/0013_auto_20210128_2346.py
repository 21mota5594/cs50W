# Generated by Django 3.1.5 on 2021-01-28 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210128_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='bidUser',
        ),
    ]
