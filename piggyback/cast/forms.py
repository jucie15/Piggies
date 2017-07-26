from django import forms
from cast.models import Comment, ReComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'add-comment', 'rows': 2}),
         }

class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment
        fields = ['message']
        widgets = {
             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
         }
