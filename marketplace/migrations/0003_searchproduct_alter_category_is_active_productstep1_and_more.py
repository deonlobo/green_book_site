# Generated by Django 5.0.6 on 2024-07-20 02:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_text', models.TextField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')]),
        ),
        migrations.CreateModel(
            name='ProductStep1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quality', models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('discounted', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Out of Stock')], max_length=1)),
                ('category', models.ManyToManyField(related_name='product_category', to='marketplace.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStep2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_upload1', models.BinaryField()),
                ('image_upload2', models.BinaryField()),
                ('image_upload3', models.BinaryField()),
                ('image_upload4', models.BinaryField()),
                ('product_step1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_step2', to='marketplace.productstep1')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStep3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textarea', models.TextField()),
                ('product_step1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_step3', to='marketplace.productstep1')),
            ],
        ),
    ]
