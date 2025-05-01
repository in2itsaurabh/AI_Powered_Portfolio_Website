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
from .forecasting_function import autots_run_pipeline
from urllib.parse import urljoin



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
            try:
                # Save file to 'media/uploads/'
                fs = FileSystemStorage(location='media/uploads/')
                filename = fs.save(csv_file.name, csv_file)
                file_path = os.path.join('media/uploads/', filename)

                # Save the path to session
                request.session['uploaded_csv_path'] = file_path

                # Read and preview data
                df = pd.read_csv(file_path)
                data_html = df.head(10).to_html(classes='table table-striped', index=False)
                columns = df.columns.tolist()

                return render(request, 'preview.html', {
                    'data_html': data_html,
                    'columns': columns
                })

            except Exception as e:
                return render(request, 'services.html', {'error': f"Error reading CSV: {str(e)}"})

    return render(request, 'services.html')





from django.http import JsonResponse
import pandas as pd
from django.conf import settings  
# def run_forecast(request):
#     if request.method == 'POST':
#         # Get form data from the POST request
#         features = request.POST.getlist('dropdown1[]')
#         target = request.POST.get('dropdown2')
#         frequency = request.POST.get('time_frame')
#         periods = int(request.POST.get('periods'))
        
#         # Assuming you've saved the CSV file path in the session
#         df = pd.read_csv(request.session.get('uploaded_csv_path'))  # Retrieve the path where the CSV is saved

#         # Run your forecasting pipeline (adjust with your forecasting function)
#         result = (df, features, target, periods, frequency)

#         # Return the result as a JSON response
#         return JsonResponse({'forecast': result})
    



from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def test_forecast_submission(request):
#     if request.method == 'POST':
#         return JsonResponse({'message': 'Hello World this my new world'})
    
import json
@csrf_exempt
def test_forecast_submission(request):
    if request.method == 'POST':
        try:
            features = request.POST.getlist('dropdown1[]')
            target = request.POST.get('dropdown2')
            frequency = request.POST.get('time_frame')
            periods = int(request.POST.get('periods'))

            # get uploaded CSV path
            file_path = request.session.get('uploaded_csv_path')
            if not file_path or not os.path.exists(file_path):
                return JsonResponse({'error': 'CSV file not found in session.'})

            df = pd.read_csv(file_path)

            # run forecast
            response, mape_score = autots_run_pipeline(df, features, target, periods, frequency)

            # save forecast CSV
            output_file_name = f"forecasted_{os.path.basename(file_path)}"
            output_path = os.path.join('media/forecasted/', output_file_name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            response.to_csv(output_path, index=False)

            # build the HTML for preview
            data_html = response.to_html(classes='table table-striped', index=False)

            result = {
                'feature': features,
                'target': target,
                'frequency': frequency,
                'periods': periods,
                'mape': mape_score,
                'forecast_csv_path': output_path,
            }

            # return both your data dict and the HTML
            relative_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
            forecast_url = urljoin(settings.MEDIA_URL, relative_path.replace(os.sep, '/'))
            # # Only extract the relative part under MEDIA_ROOT:
            # relative_path = output_path.replace(str(settings.MEDIA_ROOT) + os.sep, '')

            # # Build the public URL
            # forecast_url = settings.MEDIA_URL + relative_path.replace(os.sep, '/')

            return JsonResponse({
                'message': 'Hello World',
                'data': result,
                'data_html': data_html,
                'forecast_url': forecast_url  # <- new
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data here (e.g., send email, save message, etc.)
            form = ContactForm()  # reset the form after a successful submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
