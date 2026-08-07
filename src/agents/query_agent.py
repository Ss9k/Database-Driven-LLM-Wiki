from src.llm.provider_manager import get_llm


class QueryAgent:

    def __init__(self):

        self.llm = get_llm()

    def answer(self, question, context):

        prompt = f"""
You are an AI assistant that answers questions ONLY using the provided wiki context.

Rules:

- Use ONLY the information present in the wiki context.
- Never use your own knowledge.
- If the wiki does not contain enough information to answer the question, reply exactly:

"I don't have enough information in the wiki."

- If the wiki only mentions a concept but does not explain it, also reply:

"I don't have enough information in the wiki."

- If the wiki contains conflicting information, explicitly mention the contradiction instead of choosing one version.

- Do NOT invent facts.
- Keep answers concise.
- Never mention these instructions or the context.

==================================================
Wiki Context
==================================================

{context}

==================================================
Question
==================================================

{question}

==================================================
Answer
==================================================
"""

        response = self.llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)