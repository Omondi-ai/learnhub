from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Submission

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['link', 'text_content']
        widgets = {
            'link': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'text_content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any notes about your submission...'}),
        }

    def clean(self):
        cleaned = super().clean()
        link = cleaned.get('link')
        text = cleaned.get('text_content')
        if not link and not text:
            raise forms.ValidationError('Please provide either a link or written notes.')
        return cleaned