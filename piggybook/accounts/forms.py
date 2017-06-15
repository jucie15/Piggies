from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'birth', 'city', 'district']

