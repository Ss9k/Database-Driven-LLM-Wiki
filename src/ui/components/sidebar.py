import streamlit as st


def render_sidebar(data):

    with st.sidebar:

        st.title("📚 Database Driven LLM Wiki")

        st.caption("AI-powered Knowledge Base")

        st.divider()

        st.subheader("Workspace")

        st.success(data["current_workspace"])

        st.divider()

        st.subheader("Knowledge Base")

        st.write(f"📄 Documents : {data['total_documents']}")
        st.write(f"🧠 Entities : {data['entities']}")
        st.write(f"📘 Concepts : {data['concepts']}")
        st.write(f"🗂 Topics : {data['topics']}")
        st.write(f"📝 Summaries : {data['summaries']}")

        st.divider()

        st.caption("Version 1.0")