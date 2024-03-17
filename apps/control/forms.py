from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


# user registration form
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['department', 'fullname', 'username', 'gender', 'phone', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['comment'].required = False

    def clean_fullname(self):
        getName = self.cleaned_data['fullname']
        fullname = ' '.join(word.capitalize() for word in getName.split())
        return fullname

    def clean_username(self):
        username = self.cleaned_data['username'].capitalize()
        User = get_user_model()
        if len(username) < 3:
            raise forms.ValidationError("Username is too short.")
        if not username.isalpha():
            raise forms.ValidationError("Username should contain only alphabets A-Z.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        User = get_user_model()
        if phone and not phone.isdigit():
            raise forms.ValidationError("Please use a 10-digit phone number.")
        if phone and len(phone) != 10:
            raise forms.ValidationError("Please use a 10-digit phone number.")
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This phone number is associated with another user account.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        username = self.cleaned_data['username'].upper()
        user.set_password(username)
        if commit:
            user.save()
        return user
    
    


# User login/authentication form
class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect username or password.")
            if user.blocked:
                raise forms.ValidationError("Account blocked, contact your admin.")
            if user.deleted:
                raise forms.ValidationError("Invalid account, contact your admin.")

        return self.cleaned_data
