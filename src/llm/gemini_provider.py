import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class GeminiProvider:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def invoke(self, prompt):

        response = self.llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return response.content