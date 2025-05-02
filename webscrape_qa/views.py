from django.shortcuts import render
from .forms import WebScrapeForm
import requests
from bs4 import BeautifulSoup
from .prompt_scrap import parse_with_llm
# Global to simulate session state
extracted_text = ""

def webscrape_combined(request):
    global extracted_text
    data_extracted = False
    answer = None
    question = None
    status = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'scrape':
            form = WebScrapeForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                try:
                    res = requests.get(url)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    extracted_text = soup.get_text(separator='\n', strip=True)
                    data_extracted = True
                    status = "Data extracted successfully."
                except Exception as e:
                    status = f"Error scraping URL: {str(e)}"
        elif action == 'qa':
            form = WebScrapeForm()  # Empty form, just for layout
            question = request.POST.get('question')
            data_extracted = bool(extracted_text)
            # Replace below with real LLM logic
            # print("Extracted Text:", data_extracted)
            if data_extracted:
                # Call the LLM with the extracted text and the question
                answer = parse_with_llm(extracted_text, question)
                status = "Answer generated successfully."
            else:
                status = "No data extracted. Please scrape a URL first."
    else:
        form = WebScrapeForm()

    return render(request, 'webscrape_combined.html', {
        'form': form,
        'data': extracted_text,
        'data_extracted': data_extracted,
        'question': question,
        'answer': answer,
        'status': status
    })
