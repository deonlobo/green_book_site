# Generated by Django 5.0.6 on 2024-07-08 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_book_messenger', '0002_alter_conversation_conversation_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='conversation_type',
            field=models.CharField(choices=[('private', 'PRIVATE'), ('private_group', 'PRIVATE_GROUP'), ('public_group', 'PUBLIC_GROUP')], default='private', max_length=15),
        ),
    ]