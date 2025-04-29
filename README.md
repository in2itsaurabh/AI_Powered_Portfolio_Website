🧠 AI-Powered Portfolio Website – Full Documentation
📌 Overview
This is a Data Science Portfolio Website built using Django. It showcases AI-based tools and project capabilities through a clean user interface. The website has three main features:

🤖 Chatbot Interface – Interact with an AI to learn more about the website.

📈 Forecasting App – Upload datasets and forecast future values.

📄 RAG (Retriever-Augmented Generation) App – Upload a document and ask questions based on its contents.

🔍 Purpose
This site serves as a personal portfolio for showcasing skills in:

Machine Learning

Time Series Forecasting

Natural Language Processing

LLMs (Large Language Models)

Full Stack Web Development with Django

🗂️ Project Structure
graphql
Copy
Edit
├── manage.py                   # Django management script
├── db.sqlite3                  # Default SQLite database
├── requirements.txt            # Project dependencies
├── README.md                   # This documentation

├── home/                       # Forecasting logic & general tools
│   ├── forecasting_function.py # Core forecasting backend
│   ├── all_function.py         # Shared utilities
│   ├── forms.py                # Django forms (CSV uploads etc.)
│   └── views.py                # Views for handling forecasting and chatbot

├── rag_app/                    # RAG (Retriever-Augmented Generation) logic
│   ├── vfaissdb.py             # Vector DB logic (FAISS)
│   └── views.py                # Upload and question-answering logic

├── portfolio_site/             # Core Django project settings
│   └── settings.py             # Static files, apps, DB, etc.

├── media/
│   ├── uploads/                # User-uploaded PDFs and CSVs
│   └── forecasted/             # Forecasted results

├── static/                     # CSS & images
│   ├── css/
│   └── img/

├── templates/                  # HTML templates
│   ├── index.html              # Homepage
│   ├── services.html           # Forecasting & RAG services
│   ├── chatbot.html            # Chatbot interface
│   └── rag_interface.html      # RAG UI for upload & Q&A
🚀 Features
🤖 1. Chatbot Interface
Page: /chatbot

Description:

Users can interact with an AI chatbot embedded on the website.

It explains the website, helps you navigate features, and answers common questions.

UI is clean with animated header and styled chat window.

📈 2. Forecasting App
Page: /services (under Forecasting section)

Features:

Upload a CSV file containing time series data.

Select:

Target Variable

Frequency (Daily, Weekly, Monthly)

Period (Forecast horizon)

Uses models like XGBoost and AutoTS under the hood.

Forecast is returned and made available for download (media/forecasted/).

Helpful tooltips and loader animations are built in for better UX.

📄 3. RAG (Retriever-Augmented Generation) App
Page: /services (under RAG Application section)

Features:

Upload PDF, TXT, DOCX, or JSON files.

The system builds a vector database using FAISS and Sentence Transformers.

Ask natural language questions about the uploaded content.

Backed by RAG technique: combines search with a language model for accurate answers.

Clean UI with upload, loading indicator, and real-time responses.

📁 File Handling
All uploaded files are stored under: media/uploads/others

Forecasted CSVs saved in: media/forecasted/

Vector DBs (FAISS) are saved in: vectorstore1/

🛠️ Technologies Used

Component	Tool / Library
Framework	Django
Time Series Models	AutoTS, XGBoost
RAG Implementation	FAISS, LangChain, SentenceTransformers
Frontend	HTML, CSS, JavaScript
Chatbot Backend	OpenAI API (or local LLM support)
PDF Parsing	PyMuPDF, PyPDFLoader
Vector Embeddings	HuggingFace Transformers
📷 Screenshots
(You can add actual screenshots here if desired)

Homepage with animated chatbot banner

Services page: file uploader, forecasting options

RAG interface: PDF uploader and chat UI

📌 Future Improvements (Optional)
Add user authentication for saving past uploads and results

Deploy on Render or AWS EC2

Add more visualization for forecasts (plots, charts)

Integrate chat history in chatbot or RAG system

🔗 Deployment Notes
To run locally:

bash
Copy
Edit
git clone <repo-url>
cd <project-folder>
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Would you like me to turn this into a markdown README.md file for your project?