# Generated by Django 4.1.7 on 2024-03-17 15:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet', '0002_alter_trailer_addedby_alter_trailer_editedby_driver'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Driver',
            new_name='Truck_driver',
        ),
    ]
