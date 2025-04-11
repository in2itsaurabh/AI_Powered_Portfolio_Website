from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from .forms import ContactForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .llm_models import llm_gemini
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from.prompts import fixed_prompt
from .tools import get_calculator_tool,get_SQLquery_tool,get_Translation_tool,get_Grok_tool,get_Summarize_tool
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os


@require_POST
@csrf_protect
def chatbot_response(request):
    user_query = request.POST.get('query', '').strip().lower()
    print(user_query)
    if request.method == 'POST':
        user_query = request.POST.get('query', '')
        try:
            calculator_tool_llm = get_calculator_tool(llm=llm_gemini())
            SQLquery_tool_llm = get_SQLquery_tool(llm=llm_gemini())
            # SendEmail_tool_llm = get_SendEmail_tool(llm=llm_gemini())
            Translation_tool_llm = get_Translation_tool(llm=llm_gemini())
            Grok_tool_llm = get_Grok_tool(llm=llm_gemini())
            Summarize_tool_llm = get_Summarize_tool(llm=llm_gemini())

            tools = [calculator_tool_llm, SQLquery_tool_llm,Translation_tool_llm,Grok_tool_llm,Summarize_tool_llm]
            
            memory = ConversationBufferWindowMemory(
                memory_key='chat_history',
                k=3,
                return_messages=True
            )
            
            conversational_agent = initialize_agent(
                agent='chat-conversational-react-description',
                tools=tools,
                llm=llm_gemini(),
                verbose=True,
                max_iterations=3,
                early_stopping_method='generate',
                memory=memory
            )
            
            conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt
            response=conversational_agent(user_query)
            result=response['output']
            return JsonResponse({'output': result})


        except Exception as e:
            answer = f"Something went wrong: {str(e)}"

        return JsonResponse({'output': answer})
    

          
def home(request):
    return render(request, 'index.html')  # directly referring to 'index.html'

def services(request):
    return render(request, 'services.html')

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            # Read CSV file with pandas
            try:
                df = pd.read_csv(csv_file)
            except Exception as e:
                # Handle error if the CSV is not valid
                return render(request, 'services.html', {'error': f"Error reading CSV: {str(e)}"})

            # Convert dataframe to HTML table string
            df=df.head(10)
            data_html = df.to_html(classes='table table-striped', index=False)

            # Render a preview page to display the data
            return render(request, 'preview.html', {'data_html': data_html})
    # If GET or no CSV uploaded, return the services page
    return render(request, 'services.html')


# def process_forecast(request):
#     if request.method == "POST":
#         features = request.POST.getlist('features')
#         target = request.POST['target']
#         frequency = request.POST['frequency']
#         forecast_length = int(request.POST['forecast_length'])
        
#         # Your logic to run forecast goes here
#         return HttpResponseRedirect(request, {
#             'features': features,
#             'target': target,
#             'frequency': frequency,
#             'forecast_length': forecast_length
#         })

#     return redirect('services')





def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data here (e.g., send email, save message, etc.)
            form = ContactForm()  # reset the form after a successful submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
