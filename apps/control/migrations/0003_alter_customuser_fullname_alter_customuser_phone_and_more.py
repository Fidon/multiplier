# Generated by Django 5.0.2 on 2024-03-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_rename_description_customuser_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(error_messages={'max_length': 'Fullname is too long (max is 150).'}, max_length=150),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=None, error_messages={'max_length': 'Use a 10-digit phone number.'}, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'max_length': 'Username is too long (max is 50).'}, max_length=50, unique=True),
        ),
    ]