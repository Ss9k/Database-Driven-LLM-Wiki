import re

class ContextExtractor:

    def extract(self, document: str, keyword: str, window: int = 1):

        # Split into sentences
        sentences = re.split(
            r'(?<=[.!?])\s+',
            document.strip()
        )

        pattern = re.compile(
            rf"\b{re.escape(keyword)}\b",
            re.IGNORECASE
        )

        matches = []

        for i, sentence in enumerate(sentences):

            if pattern.search(sentence):

                start = max(0, i - window)
                end = min(len(sentences), i + window + 1)

                matches.extend(sentences[start:end])

        # Remove duplicates while preserving order
        seen = set()
        result = []

        for sentence in matches:

            sentence = sentence.strip()

            if sentence and sentence not in seen:
                seen.add(sentence)
                result.append(sentence)

        return "\n".join(result)