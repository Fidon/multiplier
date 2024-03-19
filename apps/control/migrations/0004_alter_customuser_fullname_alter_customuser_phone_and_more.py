# Generated by Django 5.0.2 on 2024-03-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_alter_customuser_fullname_alter_customuser_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]