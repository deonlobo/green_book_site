# Generated by Django 5.0.6 on 2024-07-04 04:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_book_messenger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='conversation_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
