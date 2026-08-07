import streamlit as st

st.set_page_config(
    page_title="Ask Questions",
    page_icon="🤖",
    layout="wide"
)

from services.api import get_dashboard, query
from utils.greetings import greeting
from components.chat import (
    init_chat,
    add_user_message,
    add_assistant_message,
    random_spinner,
    render_chat,
    empty_state,
    typing_animation,
)

# -------------------------------------------------------
# Initialize chat
# -------------------------------------------------------

init_chat()

# -------------------------------------------------------
# Greeting
# -------------------------------------------------------
title, subtitle = greeting()
st.title(title)
st.caption(subtitle)

# -------------------------------------------------------
# Knowledge Base Metrics
# -------------------------------------------------------
dashboard = get_dashboard()

with st.container():

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entities", dashboard["entities"])
    col2.metric("Concepts", dashboard["concepts"])
    col3.metric("Topics", dashboard["topics"])
    col4.metric("Summaries", dashboard["summaries"])

st.divider()

# -------------------------------------------------------
# Header
# -------------------------------------------------------

col1, col2 = st.columns([8, 2])

with col1:
    st.subheader("💬 Ask Questions")

with col2:
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -------------------------------------------------------
# Empty State
# -------------------------------------------------------

if len(st.session_state.messages) == 0:
    empty_state()

# -------------------------------------------------------
# Previous Chat
# -------------------------------------------------------

render_chat()

# -------------------------------------------------------
# Chat Input
# -------------------------------------------------------

question = st.chat_input(
    "Ask anything about your knowledge base..."
)

if question:

    # Store user message
    add_user_message(question)

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant
    with st.chat_message("assistant"):

        with st.spinner(random_spinner()):

            response = query(question)

        answer = response.get(
            "answer",
            "No answer generated."
        )

        sources = response.get(
            "sources",
            []
        )

        typing_animation(answer)

        # -------------------------------
        # Sources
        # -------------------------------

        if sources:

            with st.expander("📄 Sources", expanded=False):

                for src in sources:
                    st.markdown(f"- 📄 **{src}**")        

    # Save assistant response
    add_assistant_message(answer, sources)

    st.rerun()