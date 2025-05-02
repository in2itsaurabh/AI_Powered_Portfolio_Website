# webscrape_qa/forms.py
from django import forms

class WebScrapeForm(forms.Form):
    url = forms.URLField(label="Enter Website URL", widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}))
