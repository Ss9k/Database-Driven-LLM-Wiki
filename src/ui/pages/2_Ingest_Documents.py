import time

import streamlit as st

from services.api import ingest

from components.ingest import (
    upload_section,
    ingest_button,
    progress_bar,
    success_card,
    error_card,
)


st.set_page_config(
    page_title="Ingest Documents",
    page_icon="📥",
    layout="wide",
)

st.title("📥 Ingest Documents")

st.caption(
    "Expand your knowledge base by adding new markdown documents."
)

uploaded_file, source_path = upload_section()

if ingest_button():

    if uploaded_file is None:
        error_card("Please upload a Markdown or text file.")
        st.stop()

    progress, status = progress_bar()

    steps = [
        (10, "📖 Reading document"),
        (30, "🧠 Extracting knowledge"),
        (55, "📄 Creating wiki pages"),
        (75, "🔍 Updating FAISS"),
        (90, "🗂 Updating metadata"),
    ]

    try:
        for value, message in steps:
            progress.progress(value)
            status.info(message)
            time.sleep(0.4)

        response = ingest(uploaded_file)

        progress.progress(100)
        status.success("✅ Completed")

        success_card(response)

    except Exception as e:
        status.empty()
        error_card(str(e))
