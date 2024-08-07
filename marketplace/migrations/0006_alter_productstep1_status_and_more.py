# Generated by Django 5.0.6 on 2024-07-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_remove_productstep1_category_productstep1_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstep1',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Out of Stock')], default=0),
        ),
        migrations.AlterField(
            model_name='searchproduct',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='searchproduct',
            name='search_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='searchproduct',
            name='to_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
