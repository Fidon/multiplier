# Generated by Django 4.1.7 on 2024-03-16 02:01

import apps.control.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_alter_customuser_fullname_alter_customuser_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='regdate',
            field=models.DateTimeField(default=apps.control.models.dtime),
        ),
    ]