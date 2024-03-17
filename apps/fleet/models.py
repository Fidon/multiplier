from django.db import models
from apps.control.models import CustomUser
from django.utils import timezone
from datetime import timedelta


def dtime():
    return timezone.now() + timedelta(hours=3)

# trailer model
class Trailer(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    regnumber = models.CharField(max_length=16)
    trailerType = models.CharField(max_length=64)
    describe = models.TextField(null=True, default=None)
    addedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trl_registrar')
    lastEdited = models.DateTimeField(null=True, default=None)
    editedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trl_editor', null=True, default=None)
    deleted = models.BooleanField(default = False)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.regnumber)
    

# driver model
class Truck_driver(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    fullname = models.CharField(max_length=255)
    licenseNum = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    describe = models.TextField(null=True, default=None)
    addedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='dr_registrar')
    lastEdited = models.DateTimeField(null=True, default=None)
    editedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='dr_editor', null=True, default=None)
    deleted = models.BooleanField(default = False)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.fullname)
    

# truck model
class Truck(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    regnumber = models.CharField(max_length=16)
    truckType = models.CharField(max_length=255)
    horseType = models.CharField(max_length=255)
    truckModel = models.CharField(max_length=64)
    trailer = models.ForeignKey(Trailer, null=True, on_delete=models.SET_NULL, related_name='trk_trailer')
    driver = models.ForeignKey(Truck_driver, null=True, on_delete=models.SET_NULL, related_name='trk_driver')
    describe = models.TextField(null=True, default=None)
    addedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trk_registrar')
    lastEdited = models.DateTimeField(null=True, default=None)
    editedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trk_editor', null=True, default=None)
    deleted = models.BooleanField(default = False)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.regnumber)
