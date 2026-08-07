from pathlib import Path


class WikiHealthReport:

    def generate(

        self,

        broken_links,

        orphan_pages,

        duplicate_pages,

    ):

        report = []

        report.append("# Wiki Health Report\n")

        report.append(f"Broken Links : {len(broken_links)}")
        report.append(f"Orphan Pages : {len(orphan_pages)}")
        report.append(f"Duplicate Pages : {len(duplicate_pages)}")

        report.append("\n---\n")

        if broken_links:

            report.append("## Broken Links\n")

            for item in broken_links:

                report.append(
                    f"- {item['page']} -> {item['broken_link']}"
                )

            report.append("")

        if orphan_pages:

            report.append("## Orphan Pages\n")

            for page in orphan_pages:

                report.append(f"- {page}")

            report.append("")

        if duplicate_pages:

            report.append("## Duplicate Pages\n")

            for item in duplicate_pages:

                report.append(
                    f"- {item['page1']} <-> {item['page2']} ({item['score']})"
                )

        return "\n".join(report)