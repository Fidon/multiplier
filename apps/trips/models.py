from django.db import models
from apps.control.models import CustomUser
from apps.fleet.models import Truck, Trailer, Truck_driver
from django.utils import timezone
from datetime import timedelta


def dtime():
    return timezone.now() + timedelta(hours=3)

# Batch model
class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    batchnumber = models.CharField(max_length=32)
    batchType = models.CharField(max_length=32)
    client = models.CharField(max_length=255)
    describe = models.TextField(null=True, default=None)
    addedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='btc_registrar')
    lastEdited = models.DateTimeField(null=True, default=None)
    editedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='btc_editor', null=True, default=None)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.batchnumber)
    

# Trip model
class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name='trp_batch')
    truck = models.ForeignKey(Truck, on_delete=models.PROTECT, related_name='trp_truck')
    trailer = models.ForeignKey(Trailer, on_delete=models.PROTECT, related_name='trp_trailer', null=True, default=None)
    driver = models.ForeignKey(Truck_driver, on_delete=models.PROTECT, related_name='trp_driver', null=True, default=None)
    loadPoint = models.CharField(max_length=255)
    loadDate = models.DateTimeField()
    cargoWeight = models.FloatField()
    startDate = models.DateTimeField()
    destination = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    completeDate = models.DateField(null=True, default=None)
    describe = models.TextField(null=True, default=None)
    addedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trp_registrar')
    lastEdited = models.DateTimeField(null=True, default=None)
    editedBy = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='trp_editor', null=True, default=None)
    deleted = models.BooleanField(default=False)
    objects = models.Manager()
    
    def __str__(self):
        return str(f"Trip {self.id}-{self.batch}")
    
# Trip_history model
class Trip_history(models.Model):
    id = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(default=dtime)
    statusdate = models.DateField()
    tripstatus = models.CharField(max_length=255)
    newposition = models.CharField(max_length=255)
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='hist_trip')
    staff = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='hist_registrar')
    deleted = models.BooleanField(default=False)
    objects = models.Manager()
    
    def __str__(self):
        return str(f"{self.tripstatus}-{self.newposition}")
