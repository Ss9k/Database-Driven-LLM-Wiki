import streamlit as st


def render_status_card(data):

    broken = len(data["broken_links"])
    orphan = len(data["orphan_pages"])
    duplicate = len(data["duplicate_pages"])

    total = broken + orphan + duplicate

    st.subheader("Knowledge Base Status")

    if data["total_documents"] == 0:

        st.info(
            "Welcome! Start by ingesting your first document."
        )

        return

    if total == 0:

        st.success(
            "Your knowledge base is healthy."
        )

    else:

        st.warning(
            f"Your knowledge base has {total} issue(s) waiting for review."
        )

    c1, c2, c3 = st.columns(3)

    c1.metric("Broken Links", broken)

    c2.metric("Duplicates", duplicate)

    c3.metric("Orphan Pages", orphan)