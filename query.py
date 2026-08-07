from dotenv import load_dotenv

load_dotenv()

from src.workflows.query_workflow import workflow

def main():

    print("=" * 60)
    print("Database Driven LLM Wiki")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\n> ")

        if question.lower() in ["exit", "quit"]:

            print("\nGoodbye!")

            break
        from src.workspace.workspace import workspace

        print("Active project:", workspace.project_root)
        print("Entities:", list(workspace.entities.glob("*.md")))
        result = workflow.invoke(
            {
                "question": question
            }
        )

        print("\nAnswer")
        print("-" * 60)
        print(result["answer"])

        if result["sources"]:

            print("\nSources")

            for source in result["sources"]:

                print(f"- {source}")


if __name__ == "__main__":

    main()