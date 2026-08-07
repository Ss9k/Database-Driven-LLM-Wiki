from dotenv import load_dotenv

load_dotenv()

from src.llm.provider_manager import llm

response = llm.invoke(

"""
Tell me in one sentence what LangGraph is.

"""

)

print(response)