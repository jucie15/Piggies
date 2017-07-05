from django import forms
from board.models import BoardComment, Feedback

class BoardCommentForm(forms.ModelForm):
    class Meta:
        model = BoardComment
        # fields = '__all__'
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
         }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        return title

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
