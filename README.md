# 🧠 AI-Powered Portfolio Website

## 📌 Overview

This is a **Data Science Portfolio Website** built using **Django**. It showcases AI-based tools and project capabilities through a clean user interface. The website includes three main features:

1. 🤖 **Chatbot Interface** – Interact with an AI to learn more about the website.
2. 📈 **Forecasting App** – Upload datasets and forecast future values.
3. 📄 **RAG (Retriever-Augmented Generation) App** – Upload a document and ask questions based on its contents.

---

## 🔍 Purpose

This site serves as a personal portfolio to demonstrate skills in:

- Machine Learning
- Time Series Forecasting
- Natural Language Processing
- Large Language Models (LLMs)
- Full Stack Web Development using Django

---

## 🗂️ Project Structure

├── manage.py # Django management script ├── db.sqlite3 # Default SQLite database ├── requirements.txt # Project dependencies ├── README.md # Project documentation

├── home/ # Forecasting logic & tools │ ├── forecasting_function.py │ ├── all_function.py │ ├── forms.py │ └── views.py

├── rag_app/ # RAG logic │ ├── vfaissdb.py │ └── views.py

├── portfolio_site/ # Django settings │ └── settings.py

├── media/ │ ├── uploads/ # Uploaded PDFs/CSVs │ └── forecasted/ # Forecast output

├── static/ # CSS & images │ ├── css/ │ └── img/

├── templates/ # HTML templates │ ├── index.html │ ├── services.html │ ├── chatbot.html │ └── rag_interface.html




---

## 🚀 Features

### 🤖 Chatbot Interface

**URL**: `/chatbot`

- An embedded chatbot that explains website features and guides users.
- Simple and styled user interface for chat interactions.

---

### 📈 Forecasting App

**URL**: `/services` → **Forecasting Section**

- Upload a `.csv` file containing time series data.
- Choose:
  - **Target variable**
  - **Data frequency** (Daily, Weekly, Monthly)
  - **Forecast horizon**
- Uses **AutoTS** and **XGBoost** models.
- Download forecasted results from the interface.

---

### 📄 RAG App

**URL**: `/services` → **RAG Application Section**

- Upload documents: **PDF, TXT, DOCX, JSON**.
- Builds a **FAISS vector database** from content.
- Ask questions about uploaded content using **LLM-based retrieval**.
- Answers are derived from uploaded content using semantic search + LLMs.

---

## 📁 File Handling

- Uploaded files: `media/uploads/others`
- Forecasted files: `media/forecasted/`
- Vector stores: `vectorstore1/`

---

## 🛠️ Tech Stack

| Component           | Tool/Library                             |
|--------------------|-------------------------------------------|
| Backend Framework  | Django                                    |
| Forecasting        | AutoTS, XGBoost                           |
| RAG                | FAISS, LangChain, SentenceTransformers    |
| Chatbot            | OpenAI API / Local LLMs                   |
| Parsing PDFs       | PyMuPDF, PyPDFLoader                      |
| Embeddings         | HuggingFace Transformers                  |
| Frontend           | HTML, CSS, JavaScript                     |

---

## 📷 Screenshots

> _(Add your own screenshots here for UI examples)_

---

## 💡 Future Ideas

- Add user login and file history
- Deploy on Render or AWS
- Forecast visualization (charts/plots)
- Chatbot history and multi-turn support

---

## ⚙️ Run Locally

```bash
git clone <your-repo-url>
cd <project-folder>
make .env file and add your api key of gemini api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
