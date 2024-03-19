import pytz
from django.contrib.auth import authenticate, login
from django.db import models
from django.db.models.functions import Lower



def EA_TIMEZONE():
    return pytz.timezone('Etc/GMT-3')


my_timezone = EA_TIMEZONE()