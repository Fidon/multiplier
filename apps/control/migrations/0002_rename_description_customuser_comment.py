# Generated by Django 5.0.2 on 2024-03-16 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='description',
            new_name='comment',
        ),
    ]
