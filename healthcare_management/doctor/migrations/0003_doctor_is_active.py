# Generated by Django 5.1.5 on 2025-01-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
