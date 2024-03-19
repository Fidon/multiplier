# Generated by Django 4.1.7 on 2024-03-17 14:19

import apps.fleet.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='addedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trl_registrar', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='editedBy',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trl_editor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('regdate', models.DateTimeField(default=apps.fleet.models.dtime)),
                ('fullname', models.CharField(max_length=255)),
                ('licenseNum', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=32)),
                ('describe', models.TextField(default=None, null=True)),
                ('lastEdited', models.DateTimeField(default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('addedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dr_registrar', to=settings.AUTH_USER_MODEL)),
                ('editedBy', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dr_editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]