import re

from src.workspace.workspace import workspace


class OrphanPageDetector:

    def __init__(self):
        self.reload()

    def reload(self):

        self.locations = [
            workspace.entities,
            workspace.concepts,
            workspace.topics,
            workspace.summaries,
        ]

    def detect(self):

        self.reload()

        pages = {}

        referenced = set()

        pattern = r"\[\[(.*?)\]\]"

        for directory in self.locations:

            for file in directory.glob("*.md"):

                pages[file.stem] = file

        for file in pages.values():

            content = file.read_text(
                encoding="utf-8"
            )

            links = re.findall(
                pattern,
                content
            )

            referenced.update(links)

        orphan = []

        for page in pages:

            if page not in referenced:

                orphan.append(page)

        orphan.sort()

        return orphan