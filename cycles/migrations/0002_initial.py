# Generated by Django 5.1.2 on 2024-10-18 08:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cycles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cycles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cycle',
            name='supercycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cycles', to='cycles.supercycle'),
        ),
    ]
