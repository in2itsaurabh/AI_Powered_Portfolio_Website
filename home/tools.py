from langchain.tools import Tool
from langchain_core.tools import StructuredTool
from .all_function import main_calculator,main_SQLquery,main_Translate,main_GrokPattern,main_Summarize
from functools import partial
from .prompts import grok_prompt_template
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate


def get_calculator_tool(llm):
    # print("================llm math tool")
    return Tool(
        name="LLMMathCalculator",
        func=partial(main_calculator, llm=llm),
        description="Performs mathematical calculations based on user prompts using LLM."
    )



def get_SQLquery_tool(llm):
    # print("================llm sql tool")
    return Tool(
        name="LLMSQLquery",
        func=partial(main_SQLquery, llm=llm),
        description="generate SQL Query based on user input using LLM."
    )

def get_Translation_tool(llm):
    # print("================llm Translation tool")
    return Tool(
        name="LLMTranslation",
        func=partial(main_Translate, llm=llm),
        description="translate the text and give only response based on user input using LLM."
    )


def get_Grok_tool(llm):
    # print("================llm Grok tool")
    return Tool(
        name="LLMGrokPattern",
        func=partial(main_GrokPattern, llm=llm),
        description="give the observation in response"
    )


def get_Summarize_tool(llm):
    # print("================llm summarize tool")
    return Tool(
        name="LLMTextSummarize",
        func=partial(main_Summarize, llm=llm),
        description="give the observation in response"
    )

