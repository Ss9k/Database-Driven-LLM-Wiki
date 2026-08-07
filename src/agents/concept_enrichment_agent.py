from src.llm.provider_manager import get_llm


class ConceptEnrichmentAgent:

    def __init__(self):

        self.llm = get_llm()

    def enrich(self, concept: str, document: str):

        prompt = f"""
You are writing an encyclopedia-style wiki definition.

Concept

{concept}

Document

{document}

Task

Write a concise definition of ONLY this concept using ONLY the information found in the document.

Rules

- Define only the given concept.
- Do NOT summarize the document.
- Focus only on the concept.
- Use only information present in the document.
- Write 50-100 words.
- Explain what the concept is before describing its role.
- Mention related entities only if the document explicitly connects them.
- Do not invent information.
- Do not use bullet points.
- Do not repeat the concept name unnecessarily.
- If the concept is mentioned but not explained, reply exactly:

NOT_ENOUGH_INFORMATION

Return plain text only.
"""
        response = self.llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content.strip()

        return str(response).strip()