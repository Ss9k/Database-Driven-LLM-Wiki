from src.workflows.ingestion_workflow import workflow

workflow.invoke(
    {
        "source_path": "data/raw/test_article.txt"
    }
)

print("Done.")