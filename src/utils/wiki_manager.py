from pathlib import Path
from datetime import datetime
from src.database.metadata import metadata_db
from src.workspace.workspace import workspace

def entities_path():

    return workspace.entities


def concepts_path():

    return workspace.concepts


def topics_path():

    return workspace.topics


def summaries_path():

    return workspace.summaries


def index_file():

    return workspace.wiki / "index.md"


def log_file():

    return workspace.wiki / "activity.log"

def initialize_wiki():
    
    """
    Creates wiki folder structure and base files.
    """

    entities_path().mkdir(parents=True, exist_ok=True)
    concepts_path().mkdir(parents=True, exist_ok=True)
    summaries_path().mkdir(parents=True, exist_ok=True)
    topics_path().mkdir(parents=True, exist_ok=True )
     
    created = False
    if not index_file().exists():
        created = True
        index_file().write_text(
            """# Wiki Index

## Entities

None

## Concepts

None

## Summaries

None
""",
            encoding="utf-8",
        )
        

    if not log_file().exists():
        created = True
        log_file().write_text(
            "# Wiki Activity Log\n\n",
            encoding="utf-8",
        )
    if created:
        log_activity("Wiki initialized")


def log_activity(message):
    """
    Appends activity to log.md
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file(), "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def append_source(file_path: Path, source_name: str):

    content = file_path.read_text(
        encoding="utf-8"
    )

    source_line = f"- {source_name}"

    # Sources section hi nahi hai
    if "## Sources" not in content:

        content += f"\n\n## Sources\n\n{source_line}"

    else:

        # "None" ko replace karo
        if "## Sources\n\nNone" in content:

            content = content.replace(
                "## Sources\n\nNone",
                f"## Sources\n\n{source_line}"
            )

        # Already source present hai?
        elif source_line not in content:

            content += f"\n{source_line}"

    file_path.write_text(
        content,
        encoding="utf-8"
    )
    


def create_stub_page(title, source):

    file_path = entities_path() / f"{title}.md"

    if file_path.exists():

        return

    content = f"""# {title}

## Status

Stub Page

## Description

This page was automatically created during ingestion.

## Sources

- {source}
"""

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    log_activity(
        f"Created stub page: {title}"
    )
# --------------------------------------------------
# Topic Page
# --------------------------------------------------


def create_or_update_topic_page(
    topic,
    entities,
    concepts,
    summary_name,
    source
):

    file_path = topics_path() / f"{topic}.md"

    content = f"""# {topic}

## Related Summary

- {summary_name}

## Entities

"""

    for entity in entities:

        content += f"- {entity}\n"

    content += "\n## Concepts\n"

    for concept in concepts:

        content += f"- {concept}\n"

    content += """

## Sources

None
"""

    file_path.write_text(
        content,
        encoding="utf-8"
    )
    metadata_db.upsert_page( file_path, topic, "topic")

    append_source(
        file_path,
        source
    )

    log_activity(
        f"Updated topic page: {topic}"
    )

# --------------------------------------------------
# Summary Page
# --------------------------------------------------

def create_or_update_summary_page(title, summary, source):

    file_path = summaries_path() / f"{title}.md"

    action = "Updated" if file_path.exists() else "Created"

    content = f"""# {title}

## Summary

{summary}
"""

    file_path.write_text(
        content,
        encoding="utf-8"
    )
    
    metadata_db.upsert_page(
    file_path, title,"summary")

    append_source(file_path, source)

    log_activity(f"{action} summary page: {title}")


# --------------------------------------------------
# Entity Page
# --------------------------------------------------

def create_or_update_entity_page(title, summary, source):

    file_path = entities_path() / f"{title}.md"

    action = "Updated" if file_path.exists() else "Created"

    content = f"""# {title}

## Summary

{summary}

## Related Concepts

None

## Sources

None
"""

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    metadata_db.upsert_page(
        file_path,
        title,
        "entity"
    )

    append_source(
        file_path,
        source
    )

    log_activity(
        f"{action} entity page: {title}"
    )


# --------------------------------------------------
# Concept Page
# --------------------------------------------------

def create_or_update_concept_page(title, definition, source):

    file_path = concepts_path() / f"{title}.md"
    action = "Updated" if file_path.exists() else "Created"

    content = f"""# {title}

## Definition

{definition}

## Related Entities

None

## Sources

None
"""

    file_path.write_text(
            content,
            encoding="utf-8"
        )
    metadata_db.upsert_page( file_path, title, "concept")

    log_activity(
            f"Created concept page: {title}"
        )
    append_source( file_path, source)


# --------------------------------------------------
# Contradiction Handling
# --------------------------------------------------

def append_contradiction(page_name, old_claim, new_claim, explanation):
    """
    Appends contradiction information to an existing wiki page.
    """

    entity_file = entities_path() / f"{page_name}.md"
    concept_file = concepts_path() / f"{page_name}.md"

    if entity_file.exists():
        file_path = entity_file

    elif concept_file.exists():
        file_path = concept_file

    else:
        log_activity(
            f"Contradiction skipped. Page not found: {page_name}"
        )
        return

    content = file_path.read_text(
        encoding="utf-8"
    )

    if "## Contradictions" not in content:
        content += "\n\n## Contradictions\n"

    contradiction_entry = f"""

### Conflict

**Existing Claim**

{old_claim}

**New Claim**

{new_claim}

**Reason**

{explanation}

---
"""

    if contradiction_entry not in content:

        content += contradiction_entry

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        log_activity(
            f"Contradiction added to: {page_name}"
        )


# --------------------------------------------------
# Index Management
# --------------------------------------------------

def update_index():
    """
    Rebuilds index.md from wiki contents.
    """

    entities = sorted(
        [file.stem for file in entities_path().glob("*.md")]
    )

    concepts = sorted(
        [file.stem for file in concepts_path().glob("*.md")]
    )

    summaries = sorted(
        [file.stem for file in summaries_path().glob("*.md")]
    )

    topics = sorted(
    [
        file.stem
        for file in topics_path().glob("*.md")
    ])
    
    topic_section = "\n".join(

    f"- {topic}"

    for topic in topics

    ) or "None"

    entity_section = "\n".join(
        f"- {entity}" for entity in entities
    ) or "None"

    concept_section = "\n".join(
        f"- {concept}" for concept in concepts
    ) or "None"

    summary_section = "\n".join(
        f"- {summary}" for summary in summaries
    ) or "None"

    content = f"""# Wiki Index

## Entities

{entity_section}

## Concepts

{concept_section}

## Topics

{topic_section}

## Summaries

{summary_section}
"""

    index_file().write_text(
        content,
        encoding="utf-8"
    )