# Generated by Django 3.1.5 on 2021-01-28 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210127_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user',
            new_name='seller',
        ),
    ]
