from django.shortcuts import render
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

from .prompts import sql_prompt_template,translate_prompt_template,grok_prompt_template,text_summarize_prompt_template

# ==================================================CALCULATOR===========================================================
def main_calculator(input_query: str, llm) -> str:
    try:
        system_template = "You are a mathematics expert. Extract the mathematical expression from the user input and compute the answer from it. Only return the answer without any explanation."
        prompt_template = ChatPromptTemplate.from_messages([
            ('system', system_template),
            ('user', '{text}')
        ])
        parser = StrOutputParser()
        chain = prompt_template | llm | parser
        return chain
    except Exception as e:
        return f"An error occurred: {str(e)}"
            



# ==================================================SQL_QUERY===========================================================

def main_SQLquery(input_query: str, llm) -> str:
    try:
        
        sql_prompt = sql_prompt_template.format(input_query=input_query)
        return sql_prompt 
    except Exception as e:
        return f"Error during translation: {e}"
 

# ================================================== Translation ===========================================================

def main_Translate(input_query: str, llm) -> str:
    try:
        
        trans_prompt = translate_prompt_template.format(input_query=input_query)
        return trans_prompt
    except Exception as e:
        return f"Error during translation: {e}"



# ================================================== Grok Pattern ===========================================================

def main_GrokPattern(input_query: str, llm) -> str:
    try:
        groke_prompt = grok_prompt_template.format(input_query=input_query)
        return groke_prompt
    except Exception as e:
            return f"An error occurred: {str(e)}"

        

# ================================================== Text summarization ===========================================================

def main_Summarize(input_query: str, llm) -> str:
    try:
        text_summarize_prompt = text_summarize_prompt_template.format(input_query=input_query)
        return text_summarize_prompt
    except Exception as e:
            return f"An error occurred: {str(e)}"

        








# ==================================================Email Send===========================================================


