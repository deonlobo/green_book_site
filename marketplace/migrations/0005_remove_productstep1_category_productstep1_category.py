# Generated by Django 5.0.6 on 2024-07-20 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_alter_productstep1_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productstep1',
            name='category',
        ),
        migrations.AddField(
            model_name='productstep1',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='marketplace.category'),
        ),
    ]
