from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader,DirectoryLoader , TextLoader, UnstructuredWordDocumentLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from uuid import uuid4
from langchain_core.documents import Document
import os
from langchain.prompts import PromptTemplate
# from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import glob
from pathlib import Path
import sqlite3
import os 
from home.llm_models import llm_gemini

current_path = Path.cwd()


custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


def create_vector_db(filename, DB_FAISS_PATH='vectorstore1/db_faiss1', DATA_PATH='uploads/others'):
    print("this is creating the vector db")
    # Loaders for different document types
    print("Loading documents from directory...",DATA_PATH)
    pdf_loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    txt_loader = DirectoryLoader(DATA_PATH, glob='*.txt', loader_cls=TextLoader)
    docx_loader = DirectoryLoader(DATA_PATH, glob='*.docx', loader_cls=UnstructuredWordDocumentLoader)
    json_loader = DirectoryLoader(DATA_PATH, glob='*.json', loader_cls=JSONLoader)
    # print("Loading documents from directory...",docx_loader)
    # Load documents from respective loaders
    pdf_documents = pdf_loader.load()
    txt_documents = txt_loader.load()
    docx_documents = docx_loader.load()
    json_documents = json_loader.load()

    # Combine all documents into a single list
    all_documents = pdf_documents + txt_documents + docx_documents + json_documents
    print("Loaded documents:", len(all_documents))
    if not all_documents:
        print("No documents found. Ensure there are files in the specified directory.")
        return

    # Text splitting configuration
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(all_documents)

    # Create embeddings for documents
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})

    # Create a FAISS index
    db = FAISS.from_documents(texts, embeddings)

    # Ensure that the DB_FAISS_PATH's directory exists
    os.makedirs(os.path.dirname(DB_FAISS_PATH), exist_ok=True)

    # Save the FAISS database locally
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database saved at '{DB_FAISS_PATH}'")

    return f"Vector database saved at '{DB_FAISS_PATH}'"


def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return qa_chain

def load_llm():
    # llm = ChatOpenAI(model_name="MODEL_NAME", temperature=0.0,api_key=OPEN_API_KEY)
    # llm = CTransformers(
    #     model="/home/in2itadmin/Desktop/Llama2-Medical-Chatbot/llmmodel/llama-2-7b-chat.ggmlv3.q8_0.bin",
    #     model_type="llama",
    #     max_new_tokens=512,
    #     temperature=0.5
    # )
    llm = llm_gemini()
    return llm



def qa_bot(DB_FAISS_PATH):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Load FAISS vector store with dangerous deserialization allowed
    db = FAISS.load_local(
        DB_FAISS_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa


def final_result_faiss(query,DB_FAISS_PATH):
    print("=================================query+++++++++++++++++++",query)
    print("=================================DB_FAISS_PATH+++++++++++++++++++",DB_FAISS_PATH)
    qa_result = qa_bot(DB_FAISS_PATH)
    response = qa_result({'query': query})
    print("=================================response+++++++++++++++++++",response)
    return response['result']

