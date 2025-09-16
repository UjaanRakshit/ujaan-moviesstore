from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'feedback_text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)',
                'maxlength': 100
            }),
            'feedback_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about the checkout process...',
                'rows': 4,
                'required': True
            })
        }
        labels = {
            'name': 'Name (Optional)',
            'feedback_text': 'Your Feedback'
        }