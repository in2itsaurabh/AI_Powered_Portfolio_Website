from django.shortcuts import render
from .forms import SentimentForm
from .lstm_model import preprocess_and_predict  # Import your model function

def sentiment_interface(request):
    sentiment = None
    confidence = None

    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            sentiment, confidence = preprocess_and_predict(text)  # Real prediction
    else:
        form = SentimentForm()

    return render(request, 'sentiment_interface.html', {
        'form': form,
        'sentiment': sentiment,
        'confidence': confidence
    })
