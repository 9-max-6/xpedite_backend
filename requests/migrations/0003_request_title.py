# Generated by Django 5.1.2 on 2024-10-18 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='title',
            field=models.CharField(default='Default title', max_length=100),
            preserve_default=False,
        ),
    ]
