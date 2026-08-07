from pathlib import Path
import json
from src.llm.provider_manager import get_llm
from src.utils.wiki_manager import (
    entities_path,
    concepts_path,
    append_contradiction
)
llm = get_llm()
class ContradictionChecker:

    def _load_existing_page(self, page_name):

        entity_file = entities_path() / f"{page_name}.md"
        concept_file = concepts_path() / f"{page_name}.md"

        if entity_file.exists():

            return entity_file.read_text(
                encoding="utf-8"
            )

        if concept_file.exists():

            return concept_file.read_text(
                encoding="utf-8"
            )

        return None

    def check(self, page_name, new_claims):

        page_content = self._load_existing_page(
            page_name
        )

        if page_content is None:

            return

        if not new_claims:
            return
        
        prompt = f"""
        
You are a fact consistency checker.

Existing Wiki Page Content

------------------------

{page_content}

------------------------

Only compare factual statements.

Ignore formatting,
headings,
markdown syntax,
and writing style.

Only detect contradictions in facts.

------------------------

New Claims

{json.dumps(new_claims, indent=2)}

Your task:

Compare the new claims with the existing wiki page.

If there is NO contradiction return ONLY

{{
    "contradiction": false
}}

If there IS contradiction return ONLY valid JSON

{{
    "contradiction": true,
    "old_claim": "...",
    "new_claim": "...",
    "reason": "..."
}}

Do not return markdown.

Do not explain.

Return JSON only.
"""

        

        response_text = llm.invoke(prompt).strip()

        if response_text.startswith("```"):

            response_text = (
                response_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        try:

            result = json.loads(response_text)

        except json.JSONDecodeError:

            print("Invalid JSON from LLM")
            print(response_text)
            return

        if not result.get("contradiction",False):
            return

        append_contradiction(
            page_name,
            result.get("old_claim", ""),
            result.get("new_claim", ""),
            result.get("reason", ""),
        )