import json

from dotenv import load_dotenv

from src.llm.provider_manager import get_llm

load_dotenv()

llm = get_llm()


class ExtractionAgent:

    def extract(self, text: str):

        prompt = f"""
You are an information extraction system.

Your ONLY job is to identify information.

Do NOT summarize.

Do NOT explain entities.

Do NOT define concepts.

Return ONLY raw JSON.

No markdown.

No explanations.

No ```json.

Schema:

{{
    "entities": [
        "..."
    ],

    "concepts": [
        "..."
    ],

    "claims": [
        "..."
    ]
}}

Rules:

- entities = proper nouns, technologies, people, organizations, products, named biological objects etc.

- concepts = abstract ideas, scientific concepts, algorithms, methods, theories, processes.

- claims = important factual statements from the document.

Return valid JSON only.

Document:

{text}
"""

        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            response = response.content

        return json.loads(response)