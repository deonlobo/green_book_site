# Generated by Django 5.0.6 on 2024-07-17 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DIYProject', '0005_alter_project_tools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
