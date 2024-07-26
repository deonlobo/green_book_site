# Generated by Django 5.0.7 on 2024-07-26 05:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DIYProject', '0009_favourite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='diyproject_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
