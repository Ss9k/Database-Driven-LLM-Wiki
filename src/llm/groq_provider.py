import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
load_dotenv()


class GroqProvider:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def invoke(self, prompt):

        response = self.llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return response.content
