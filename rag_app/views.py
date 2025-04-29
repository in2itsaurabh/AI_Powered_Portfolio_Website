from django.shortcuts import render
from django.http import JsonResponse
import time
from .vfaissdb import create_vector_db, final_result_faiss
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# View for RAG Interface page
def rag_interface(request):
    return render(request, 'rag_interface.html')

# Simulating PDF file processing (with delay)
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        print(f"Received file: {pdf_file.name}")
        
        # Define the directory where you want to save the file
        upload_directory = 'uploads/others'
        
        # Ensure that the upload directory exists
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Save the uploaded file to the directory
        fs = FileSystemStorage(location=upload_directory)
        filename = fs.save(pdf_file.name, pdf_file)
        print(f"File saved: {filename}")
        file_path = fs.url(filename) 
        
        # ===> Save filename to session
        request.session['uploaded_pdf'] = filename
        
        res = create_vector_db(filename, f'vectorstore1/{filename}', upload_directory)
        return JsonResponse({'success': True, 'file_path': file_path})

    else:
        return JsonResponse({'success': False, 'error': 'No file uploaded or invalid request.'})


# Handle the question
def ask_question(request):
    if request.method == 'POST':
        query = request.POST.get('question')
        
        # Get the filename from the session
        filename = request.session.get('uploaded_pdf')
        print("filename", filename)
        if filename:
            DB_FAISS_PATH = f'vectorstore1/{filename}'
            response = final_result_faiss(query, DB_FAISS_PATH)
            
            # Return the answer from the FAISS database query
            return JsonResponse({'answer': response})
        else:
            return JsonResponse({'error': 'No file uploaded or session expired'}, status=400)
    return JsonResponse({'error': 'No question provided'}, status=400)
