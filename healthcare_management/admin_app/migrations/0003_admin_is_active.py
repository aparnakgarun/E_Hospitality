# Generated by Django 5.1.5 on 2025-01-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
