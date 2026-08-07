import streamlit as st


def upload_section():

    st.subheader("📥 Upload Markdown")

    uploaded_file = st.file_uploader(
        "Choose a markdown file",
        type=["md"]
    )

    st.markdown("### OR")

    source_path = st.text_input(
        "Existing File Path",
        placeholder="data/source/test_article.md"
    )

    return uploaded_file, source_path


def ingest_button():

    return st.button(
        "🚀 Ingest Document",
        use_container_width=True,
        type="primary"
    )


def progress_bar():

    progress = st.progress(0)

    status = st.empty()

    return progress, status


def success_card(response):

    st.success("Document Successfully Ingested")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Summary",
            response.get("summary", 1)
        )

        st.metric(
            "Topics",
            response.get("topics", 1)
        )

        st.metric(
            "Entities",
            response.get("entities", 0)
        )

    with col2:

        st.metric(
            "Concepts",
            response.get("concepts", 0)
        )

        st.metric(
            "FAISS",
            response.get(
                "faiss",
                "Updated"
            )
        )

        st.metric(
            "Metadata",
            response.get(
                "metadata",
                "Updated"
            )
        )


def error_card(message):

    st.error(message)