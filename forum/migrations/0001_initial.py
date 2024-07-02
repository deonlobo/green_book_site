# Generated by Django 5.0.6 on 2024-07-02 05:55

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(default='DEFAULT_ID', max_length=500, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('body', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('tags', models.ManyToManyField(related_name='questions', to='forum.tag')),
            ],
        ),
    ]
