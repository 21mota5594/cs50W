# Generated by Django 3.1.5 on 2021-01-29 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210129_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.CharField(default='', max_length=1500),
        ),
        migrations.AddField(
            model_name='comment',
            name='commentListing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commentUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
