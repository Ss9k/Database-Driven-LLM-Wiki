import streamlit as st

from services.api import browse, get_page

st.set_page_config(
    page_title="Browse Wiki",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Browse Wiki")

category = st.sidebar.selectbox(
    "Category",
    [
        "entities",
        "concepts",
        "topics",
        "summaries",
    ],
)

data = browse(category)

pages = data.get("pages", [])

if not pages:

    st.info("No pages available.")

    st.stop()

selected = st.sidebar.selectbox(
    "Pages",
    pages,
)

page = get_page(
    category,
    selected,
)

st.subheader(page["title"])

st.markdown(page["content"])