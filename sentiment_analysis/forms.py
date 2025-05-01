# sentiment_analysis/forms.py
from django import forms

class SentimentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'cols': 50, 
            'placeholder': 'Enter your text...'
        }),
        label='',
        max_length=1000
    )
