# Generated by Django 5.0.6 on 2024-07-22 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_book_challenges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='deadline',
            field=models.DateField(default='2024-12-31'),
            preserve_default=False,
        ),
    ]