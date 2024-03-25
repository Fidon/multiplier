from django import forms
from .models import Batch, Trip, Trip_history

# new batch form
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batchnumber', 'batchType', 'client', 'describe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['describe'].required = False

    def clean_batchnumber(self):
        batchnumber = self.cleaned_data.get('batchnumber').strip().capitalize()
        if len(batchnumber) < 6:
            raise forms.ValidationError("Batch number is too short.")
        if self.instance and self.instance.pk:
            if Batch.objects.filter(batchnumber=batchnumber, deleted=False).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This batch number is already registered.")
        else:
            if Batch.objects.filter(batchnumber=batchnumber, deleted=False).exists():
                raise forms.ValidationError("This batch number is already registered.")
        return batchnumber
    
    def clean_client(self):
        client = self.cleaned_data.get('client').strip()
        return client
    
    def clean_describe(self):
        describe = self.cleaned_data.get('describe').strip()
        if describe in ("", "-"):
            return None
        return describe
    
# new trip form
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['batch', 'truck', 'loadPoint', 'loadDate', 'cargoWeight', 'startDate', 'destination', 'completed', 'completeDate', 'describe', 'trailer', 'driver']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trailer'].required = False
        self.fields['driver'].required = False
        self.fields['completeDate'].required = False
        self.fields['describe'].required = False

    def clean_loadPoint(self):
        loadPoint = self.cleaned_data.get('loadPoint').strip()
        if len(loadPoint) < 3:
            raise forms.ValidationError("Load point is too short.")
        return loadPoint

    def clean_destination(self):
        destination = self.cleaned_data.get('destination').strip()
        if len(destination) < 3:
            raise forms.ValidationError("Destination is too short.")
        return destination
    
    def clean_describe(self):
        describe = self.cleaned_data.get('describe').strip()
        if describe in ("", "-"):
            return None
        return describe

# new trip_history form
class Trip_historyForm(forms.ModelForm):
    class Meta:
        model = Trip_history
        fields = ['tripstatus', 'newposition', 'statusdate', 'trip']

    def clean_tripstatus(self):
        tripstatus = self.cleaned_data.get('tripstatus').strip()
        if len(tripstatus) < 3:
            raise forms.ValidationError("Status is too short.")
        return tripstatus

    def clean_newposition(self):
        newposition = self.cleaned_data.get('newposition').strip()
        if len(newposition) < 3:
            raise forms.ValidationError("Position is too short.")
        return newposition
