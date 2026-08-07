from src.llm.provider_manager import get_llm


class SummaryAgent:

    def __init__(self):

        self.llm = get_llm()

    def generate(self, document: str):

        prompt = f"""
You are writing a concise encyclopedia-style summary.

Write ONE high-quality summary of the document.

Rules:

- 120-180 words
- Explain the main topic.
- The summary should be understandable without reading the original document.
- Avoid repeating the document title.
- Mention important entities naturally.
- Preserve factual accuracy.
- Do not invent information.
- Do not use bullet points.
- Output only the summary.

Document:

{document}
"""

        response = self.llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)