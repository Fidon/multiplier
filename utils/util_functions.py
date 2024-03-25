import pytz
from django.contrib.auth import authenticate, login
from django.db import models
from django.db.models.functions import Lower



def EA_TIMEZONE():
    return pytz.timezone('Etc/GMT-3')

# format truck or trailer reg number
def format_reg(regnumber):
    return f"{regnumber[:1]} {regnumber[1:4]} {regnumber[4:]}"

# format driver's license number'
def format_license(num):
    return f"{num[:4]} {num[4:8]} {num[8:]}"

# format phone number
def format_phone(num):
    return f"{num[:4]}-{num[4:7]}-{num[7:]}"

