# Generated by Django 4.1.7 on 2024-03-17 16:31

import apps.fleet.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet', '0003_rename_driver_truck_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('regdate', models.DateTimeField(default=apps.fleet.models.dtime)),
                ('regnumber', models.CharField(max_length=16)),
                ('truckType', models.CharField(max_length=255)),
                ('horseType', models.CharField(max_length=255)),
                ('truckModel', models.CharField(max_length=64)),
                ('describe', models.TextField(default=None, null=True)),
                ('lastEdited', models.DateTimeField(default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('addedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trk_registrar', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trk_driver', to='fleet.truck_driver')),
                ('editedBy', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trk_editor', to=settings.AUTH_USER_MODEL)),
                ('trailer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trk_trailer', to='fleet.trailer')),
            ],
        ),
    ]