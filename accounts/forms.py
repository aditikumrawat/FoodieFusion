from typing import Any
from django import forms
from .models import User, UserProfile
from .validator import only_allow_images

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("first_name", "last_name","username","email", 'password')

    def clean(self):
       clean_data = super(UserForm, self).clean()
       password = clean_data.get('password')
       confirm_password = clean_data.get('confirm_password')

       if password != confirm_password:
           raise forms.ValidationError("Password does not match!")
       
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Start typing.....", "required": "required"}))
    profile_picture = forms.CharField(widget=forms.FileInput(attrs= {'class':'btn btn-info'}), validators=[only_allow_images,]) 
    cover_photo = forms.FileField(widget=forms.FileInput(attrs= {'class':'btn btn-info'}), validators= [only_allow_images,])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs= {'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs= {'readonly':'readonly'}))
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pincode', 'latitude', 'longitude']
     
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'longitude' or field == 'latitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                
                
                
                