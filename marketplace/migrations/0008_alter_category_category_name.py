# Generated by Django 5.0.7 on 2024-07-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0007_alter_category_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
