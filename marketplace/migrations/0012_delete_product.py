# Generated by Django 5.0.6 on 2024-07-26 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0011_productstep2_created_at_productstep2_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
