# Generated by Django 4.1.7 on 2024-03-16 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_department_regdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='regdate',
        ),
    ]