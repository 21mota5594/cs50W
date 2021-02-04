# Generated by Django 3.1.5 on 2021-01-29 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210128_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='bid',
            name='bidUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='bids',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.bid'),
        ),
    ]