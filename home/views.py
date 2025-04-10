from django.shortcuts import render
from .forms import ContactForm

def home(request):
    return render(request, 'index.html')  # directly referring to 'index.html'

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data here (e.g., send email, save message, etc.)
            form = ContactForm()  # reset the form after a successful submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
