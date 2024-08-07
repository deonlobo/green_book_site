# Generated by Django 5.0.7 on 2024-08-05 17:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_book_messenger', '0005_message_username'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='pinned',
        ),
        migrations.AddField(
            model_name='conversation',
            name='pinned',
            field=models.ManyToManyField(blank=True, related_name='pinned_conversations', to=settings.AUTH_USER_MODEL),
        ),
    ]
