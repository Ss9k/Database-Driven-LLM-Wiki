import time
from pathlib import Path

import streamlit as st

from services.api import ingest

from components.ingest import (
    upload_section,
    ingest_button,
    progress_bar,
    success_card,
    error_card,
)

SOURCE_FOLDER = Path("data/source")

SOURCE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

st.set_page_config(
    page_title="Ingest Documents",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Ingest Documents")

st.caption(
    "Expand your knowledge base by adding new markdown documents."
)

uploaded_file, source_path = upload_section()

if ingest_button():

    if uploaded_file is not None:

        save_path = (
            SOURCE_FOLDER
            / uploaded_file.name
        )

        with open(
            save_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        final_path = str(save_path)

    elif source_path:

        final_path = source_path

    else:

        error_card(
            "Please upload a markdown file or provide a source path."
        )

        st.stop()

    progress, status = progress_bar()

    steps = [

        (10, "📖 Reading document"),

        (30, "🧠 Extracting knowledge"),

        (55, "📄 Creating wiki pages"),

        (75, "🔍 Updating FAISS"),

        (90, "🗂 Updating metadata"),

    ]

    for value, text in steps:

        progress.progress(value)

        status.info(text)

        time.sleep(0.4)

    try:

        response = ingest(
            final_path
        )

        progress.progress(100)

        status.success(
            "✅ Completed"
        )

        success_card(response)

    except Exception as e:

        error_card(str(e))