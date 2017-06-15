from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import Profile
from tagging.forms import TagField

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'birth', 'city', 'district']

class TagForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['tag']
