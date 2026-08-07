import streamlit as st


def render_metrics(data):

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="📄 Documents",
            value=data["total_documents"],
        )

        st.metric(
            label="📘 Concepts",
            value=data["concepts"],
        )

    with col2:

        st.metric(
            label="🧠 Entities",
            value=data["entities"],
        )

        st.metric(
            label="🗂 Topics",
            value=data["topics"],
        )