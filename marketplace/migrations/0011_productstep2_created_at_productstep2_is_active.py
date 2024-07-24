# Generated by Django 5.0.7 on 2024-07-23 04:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0010_productstep3_created_at_productstep3_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productstep2',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='productstep2',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
