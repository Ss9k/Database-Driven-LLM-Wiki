from src.llm.provider_manager import get_llm


class EntityEnrichmentAgent:

    def __init__(self):

        self.llm = get_llm()

    def enrich(self, entity: str, document: str):

        prompt = f"""
You are writing a Wikipedia article.

Target Entity:
{entity}

Context:
{document}

Your task is to write a standalone encyclopedia entry ONLY about the target entity.

Rules:

1. The FIRST sentence MUST define "{entity}".
2. Never define another entity instead.
3. Use surrounding context only to explain the target entity.
4. Ignore information that is not directly related to "{entity}".
5. Do NOT summarize the whole context.
6. Do NOT describe the document.
7. If another concept is needed to explain "{entity}", mention it briefly.
8. Use only information from the context.
9. 60-120 words.
10. No markdown.
11. No bullet points.
12. Never invent information.

If the context does not actually explain "{entity}",
return exactly:

NOT_ENOUGH_INFORMATION

Return only the encyclopedia entry.
"""
        
        response = self.llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content.strip()

        return str(response).strip()