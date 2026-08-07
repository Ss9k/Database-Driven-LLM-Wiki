import time
import streamlit as st
import random

spinner_messages = [

    "Thinking...",

    "Searching your wiki...",

    "Reading markdown pages...",

    "Comparing documents...",

    "Building answer...",

    "Checking knowledge base...",

    "Looking through concepts...",

    "Analyzing relationships..."

]


def random_spinner():

    return random.choice(spinner_messages)

def init_chat():
    """Initialize chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_user_message(message):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )


def add_assistant_message(message, sources=None):
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message,
            "sources": sources or []
        }
    )


def render_chat():

    for idx, msg in enumerate(st.session_state.messages):

        if msg["role"] == "user":

            with st.chat_message("user"):
                st.markdown(msg["content"])

        else:

            with st.chat_message("assistant"):

                st.markdown(msg["content"])

                # Copy Answer
                with st.expander("📋 Copy Answer", expanded=False):

                    st.code(
                        msg["content"],
                        language=None
                    )

                # Sources
                if msg.get("sources"):

                    with st.expander("📄 Sources", expanded=False):

                        for source in msg["sources"]:

                            st.markdown(
                                f"📘 **{source}**"
                            )


def empty_state():

    st.markdown(
        """
# Ask anything about your wiki.

### Try asking

- What is LangGraph?
- Explain RAG
- Summarize Quantum Computing
"""
    )

def typing_animation(answer, speed=0.01):

    placeholder = st.empty()

    current = ""

    for ch in answer:

        current += ch

        placeholder.markdown(current)

        time.sleep(speed)

    return placeholder