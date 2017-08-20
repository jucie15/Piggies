from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from accounts.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'nickname', 'sex', 'birth', 'city', 'district']
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "textinput form-control"}),
            "sex": forms.Select(attrs={"class": "select form-control"}),
            "birth": forms.TextInput(attrs={"name": "birth", "class": "textinput form-control", "placeholder": "예: 19801230"}),
            "city": forms.Select(attrs={"id": "city", "name": "city", "class": "form-control"}),
            "district": forms.Select(attrs={"id": "district", "name": "district", "class": "form-control"}),
        }
        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

        def clean_sex(self):
            sex = self.cleaned_data.get('sex','')
            return sex

        def clean_birth(self):
            birth = self.cleaned_data.get('birth','')
            return birth

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data

