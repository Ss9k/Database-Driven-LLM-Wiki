from pathlib import Path
import re
from src.utils.wiki_manager import (
    entities_path,
    concepts_path,
    topics_path,
    summaries_path,
)


class WikiSearch:

    def __init__(self):
        self.reload()
    
    def reload(self):
        self.search_locations = {
            "entity": entities_path(),
            "concept": concepts_path(),
            "topic": topics_path(),
            "summary": summaries_path(),
        }
        


    def _search_directory(self, directory, page_type, query):
        
        results = []
        
        STOP_WORDS = {
                "what", "where", "when", "which", "who",
                "why", "how", "the", "and", "for",
                "with", "this", "that", "from"
            }  
        
        query = query.lower()
        words = re.findall(r"\w+", query)

        for file in directory.glob("*.md"):

            content = file.read_text(
                encoding="utf-8"
            )

            score = 0

            filename = file.stem.lower()

            content_lower = content.lower()

            for word in words:
                
                             
                if word in STOP_WORDS:
                    continue


                if len(word) < 3:
                    continue

                if word in filename:
                    score += 5

                score += content_lower.count(word)
            
            if score > 0:

                results.append(
                    {
                        "title": file.stem,
                        "type": page_type,
                        "content": content,
                        "path": str(file),
                        "score": score,
                    }
                )

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return results

    def search_entities(self, query):

        return self._search_directory(
            self.search_locations["entity"],
            "entity",
            query,
        )

    def search_concepts(self, query):

        return self._search_directory(
            self.search_locations["concept"],
            "concept",
            query,
        )

    def search_topics(self, query):

        return self._search_directory(
            self.search_locations["topic"],
            "topic",
            query,
        )

    def search_summaries(self, query):

        return self._search_directory(
            self.search_locations["summary"],
            "summary",
            query,
        )

    def retrieve_documents(self, query):
        self.reload()
        documents = []

        documents.extend(
            self.search_entities(query)
        )

        documents.extend(
            self.search_concepts(query)
        )

        documents.extend(
            self.search_topics(query)
        )

        documents.extend(
            self.search_summaries(query)
        )

        documents.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return documents