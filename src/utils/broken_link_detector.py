import re

from src.workspace.workspace import workspace


class BrokenLinkDetector:

    def __init__(self):
        self.reload()

    def reload(self):

        self.locations = [
            workspace.entities,
            workspace.concepts,
            workspace.topics,
            workspace.summaries,
        ]

    def _all_pages(self):

        pages = set()

        for directory in self.locations:

            for file in directory.glob("*.md"):

                pages.add(file.stem)

        return pages

    def detect(self):

        self.reload()

        existing_pages = self._all_pages()

        broken = []

        pattern = r"\[\[(.*?)\]\]"

        for directory in self.locations:

            for file in directory.glob("*.md"):

                content = file.read_text(
                    encoding="utf-8"
                )

                links = re.findall(
                    pattern,
                    content
                )

                for link in links:

                    if link not in existing_pages:

                        broken.append(
                            {
                                "page": file.stem,
                                "broken_link": link,
                            }
                        )

        return broken