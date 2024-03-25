from django import forms
from .models import Trailer, Truck_driver, Truck

# new trailer registartion form
class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = ['regnumber', 'trailerType', 'describe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['describe'].required = False

    def clean_regnumber(self):
        reg = self.cleaned_data.get('regnumber').strip().upper()
        regnumber = ''.join(reg.split())
        if len(regnumber) < 7:
            raise forms.ValidationError("Reg number is too short.")
        if self.instance and self.instance.pk:
            if Trailer.objects.filter(regnumber=regnumber, deleted=False).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This trailer number is already registered.")
        else:
            if Trailer.objects.filter(regnumber=regnumber, deleted=False).exists():
                raise forms.ValidationError("This trailer number is already registered.")
        return regnumber
    
    def clean_describe(self):
        describe = self.cleaned_data.get('describe').strip()
        if describe in ("", "-"):
            return None
        return describe
    

# new driver registration form
class Truck_driverForm(forms.ModelForm):
    class Meta:
        model = Truck_driver
        fields = ['fullname', 'licenseNum', 'phone', 'describe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['describe'].required = False

    def clean_fullname(self):
        getName = self.cleaned_data['fullname'].strip()
        fullname = ' '.join(word.capitalize() for word in getName.split())
        return fullname

    def clean_licenseNum(self):
        lic_num = self.cleaned_data.get('licenseNum').strip()
        licenseNum = ''.join(lic_num.split())
        if not licenseNum.isdigit():
            raise forms.ValidationError("License should have only numbers.")
        if len(licenseNum) < 8:
            raise forms.ValidationError("Licence number is too short.")
        if self.instance and self.instance.pk:
            if Truck_driver.objects.filter(licenseNum=licenseNum, deleted=False).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This license is associated with another driver.")
        else:
            if Truck_driver.objects.filter(licenseNum=licenseNum, deleted=False).exists():
                raise forms.ValidationError("This license is associated with another driver.")
        return licenseNum
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if not phone.isdigit():
            raise forms.ValidationError("Please use a 10-digit phone number.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number should have 10 digits.")
        if self.instance and self.instance.pk:
            if Truck_driver.objects.filter(phone=phone, deleted=False).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This phone number is associated with another driver.")
        else:
            if Truck_driver.objects.filter(phone=phone, deleted=False).exists():
                raise forms.ValidationError("This phone number is associated with another driver.")
        return phone
    
    def clean_describe(self):
        describe = self.cleaned_data.get('describe').strip()
        if describe in ("", "-"):
            return None
        return describe


# new truck registartion form
class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['regnumber', 'truckType', 'horseType', 'truckModel', 'trailer', 'driver', 'describe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trailer'].required = False
        self.fields['driver'].required = False
        self.fields['describe'].required = False

    def clean_regnumber(self):
        reg = self.cleaned_data.get('regnumber').strip().upper()
        regnumber = ''.join(reg.split())
        if len(regnumber) < 7:
            raise forms.ValidationError("Reg number is too short.")
        if self.instance and self.instance.pk:
            if Truck.objects.filter(regnumber=regnumber, deleted=False).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This truck number is already registered.")
        else:
            if Truck.objects.filter(regnumber=regnumber, deleted=False).exists():
                raise forms.ValidationError("This truck number is already registered.")
        return regnumber
    
    def clean_truckType(self):
        truckType = self.cleaned_data.get('truckType').strip()
        return truckType
    
    def clean_truckModel(self):
        truckModel = self.cleaned_data.get('truckModel').strip()
        return truckModel
    
    def clean_trailer(self):
        trailer = self.cleaned_data.get('trailer')
        if self.instance and self.instance.pk:
            same_trailer = Truck.objects.filter(trailer=trailer, deleted=False)\
                .exclude(pk=self.instance.pk)\
                .exclude(trailer__isnull=True)
            if same_trailer.exists():
                raise forms.ValidationError("This trailer is already assigned to another truck.")
        else:
            if Truck.objects.filter(trailer=trailer, deleted=False).exists():
                raise forms.ValidationError("This trailer is already assigned to another truck.")
        if trailer == "":
            return None
        return trailer
    
    def clean_driver(self):
        driver = self.cleaned_data.get('driver')
        if self.instance and self.instance.pk:
            same_driver = Truck.objects.filter(driver=driver, deleted=False)\
                .exclude(pk=self.instance.pk)\
                .exclude(driver__isnull=True)
            if same_driver.exists():
                raise forms.ValidationError("This driver is already assigned to another truck.")
        else:
            if Truck.objects.filter(driver=driver, deleted=False).exists():
                raise forms.ValidationError("This driver is already assigned to another truck.")
        if driver == "":
            return None
        return driver
    
    def clean_describe(self):
        describe = self.cleaned_data.get('describe').strip()
        if describe in ("", "-"):
            return None
        return describe
