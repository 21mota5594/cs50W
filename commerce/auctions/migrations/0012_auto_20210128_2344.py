# Generated by Django 3.1.5 on 2021-01-28 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_listing_currentbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.listing'),
        ),
    ]
