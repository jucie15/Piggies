from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import Profile
from tagging.forms import TagField

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'sex', 'birth', 'city', 'district']
        widgets = {
            "sex": forms.Select(attrs={"class":"form-control"}),
            "birth": forms.TextInput(attrs={"class":"form-control"}),
            "city": forms.HiddenInput(),
            "district": forms.HiddenInput(),
        }

        def clean_sex(self):
            sex = self.cleaned_data.get('sex','')
            return sex

        def clean_birth(self):
            birth = self.cleaned_data.get('birth','')
            return birth

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data


class TagForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['tag']
