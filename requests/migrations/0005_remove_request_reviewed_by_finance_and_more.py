# Generated by Django 5.1.2 on 2024-10-20 11:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_remove_request_reviewed_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='reviewed_by_finance',
        ),
        migrations.RemoveField(
            model_name='request',
            name='reviewed_by_sup',
        ),
        migrations.AddField(
            model_name='request',
            name='reviewed_by_finance',
            field=models.ManyToManyField(blank=True, related_name='reviewed_requests_finance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='reviewed_by_sup',
            field=models.ManyToManyField(blank=True, related_name='reviewed_requests_sup', to=settings.AUTH_USER_MODEL),
        ),
    ]
