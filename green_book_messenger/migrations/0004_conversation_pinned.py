# Generated by Django 5.0.6 on 2024-07-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_book_messenger', '0003_conversation_conversation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='pinned',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
