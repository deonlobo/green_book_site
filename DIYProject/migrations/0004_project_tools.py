# Generated by Django 5.0.6 on 2024-07-17 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DIYProject', '0003_alter_project_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tools',
            field=models.CharField(default='Plastic containers', max_length=200),
        ),
    ]