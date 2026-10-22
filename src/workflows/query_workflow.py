# from typing import TypedDict

# from langgraph.graph import StateGraph, END

# from src.utils.wiki_search import WikiSearch
# from src.query.context_builder import ContextBuilder
# from src.agents.query_agent import QueryAgent
# from src.query.hybrid_search import HybridSearch

# search = HybridSearch()
# builder = ContextBuilder()
# agent = QueryAgent()


# class QueryState(TypedDict):

#     question: str

#     documents: list

#     context: str

#     sources: list

#     answer: str


# def search_node(state: QueryState):
#     query = (
#         state["question"]
#         .lower()
#         .replace("what is", "")
#         .replace("who is", "")
#         .replace("define", "")
#         .replace("?", "")
#         .strip()
#     )
#     documents = search.search(query)

#     print("\nRetrieved Documents:")
#     for doc in documents:
#         print(doc["title"], doc["path"], doc["score"])

#     state["documents"] = documents
#     documents = search.search(query)

#     state["documents"] = documents

#     return state


# def context_node(state: QueryState):

#     result = builder.build_context(state["documents"])

#     state["context"] = result["context"]
#     state["sources"] = result["sources"]


#     return state


# def answer_node(state: QueryState):

#     state["answer"] = agent.answer(

#         state["question"],

#         state["context"]

#     )
#     answer = state["answer"].lower()

#     if (
#         "don't have enough information" in answer
#         or
#         "not enough information" in answer
#     ):

#         state["sources"] = []



#     return state


# graph = StateGraph(QueryState)

# graph.add_node("search", search_node)

# graph.add_node("context", context_node)

# graph.add_node("answer", answer_node)

# graph.set_entry_point("search")

# graph.add_edge("search", "context")

# graph.add_edge("context", "answer")

# graph.add_edge("answer", END)

# workflow = graph.compile()


from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.query.context_builder import ContextBuilder
from src.agents.query_agent import QueryAgent
from src.query.hybrid_search import HybridSearch

search = HybridSearch()
builder = ContextBuilder()
agent = QueryAgent()


class QueryState(TypedDict):
    question: str
    documents: list
    context: str
    sources: list
    answer: str


def is_greeting(question: str) -> bool:
    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
        "how are you",
        "how are you?",
        "what's up",
        "whats up",
        "thank you",
        "thanks",
    }

    normalized = question.lower().strip().rstrip("!.,")

    return normalized in greetings


def greeting_node(state: QueryState):
    state["answer"] = (
        "Hello! 👋 I'm your AI Wiki assistant. "
        "I can help you explore documents, entities, and "
        "concepts in your knowledge base. What would you "
        "like to know?"
    )
    state["documents"] = []
    state["context"] = ""
    state["sources"] = []

    return state


def search_node(state: QueryState):
    query = (
        state["question"]
        .lower()
        .replace("what is", "")
        .replace("who is", "")
        .replace("define", "")
        .replace("?", "")
        .strip()
    )

    documents = search.search(query)

    print("\nRetrieved Documents:")
    for doc in documents:
        print(doc["title"], doc["path"], doc["score"])

    state["documents"] = documents

    return state


def context_node(state: QueryState):
    result = builder.build_context(state["documents"])

    state["context"] = result["context"]
    state["sources"] = result["sources"]

    return state


def answer_node(state: QueryState):
    state["answer"] = agent.answer(
        state["question"],
        state["context"],
    )

    answer = state["answer"].lower()

    if (
        "don't have enough information" in answer
        or "not enough information" in answer
    ):
        state["sources"] = []

    return state


def route_query(state: QueryState):
    if is_greeting(state["question"]):
        return "greeting"

    return "search"


graph = StateGraph(QueryState)

graph.add_node("router", lambda state: state)
graph.add_node("greeting", greeting_node)
graph.add_node("search", search_node)
graph.add_node("context", context_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route_query,
    {
        "greeting": "greeting",
        "search": "search",
    },
)

graph.add_edge("greeting", END)
graph.add_edge("search", "context")
graph.add_edge("context", "answer")
graph.add_edge("answer", END)

workflow = graph.compile()
