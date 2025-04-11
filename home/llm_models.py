from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import logging

# Set up logging for better debugging
logger = logging.getLogger(__name__)



def llm_gemini():
    llm_gemini_obj = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0,
            )
    return llm_gemini_obj
