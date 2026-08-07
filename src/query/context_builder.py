from pathlib import Path


class ContextBuilder:

    def build_context(self, documents):

        if not documents:

            return {
                "context": "No relevant information found.",
                "sources": []
            }

        context = ""

        sources = []

        for doc in documents:

            context += (
                f"\n===== {doc['title']} "
                f"({doc['type']}) =====\n\n"
            )

            try:

                content = Path(doc["path"]).read_text(
                    encoding="utf-8"
                )

            except Exception:

                content = "Unable to read page."

            context += content

            context += "\n\n"

            sources.append(doc["title"])

        # Remove duplicate sources while preserving order
        sources = list(dict.fromkeys(sources))

        return {
            "context": context,
            "sources": sources
        }