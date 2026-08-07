from datetime import datetime

import streamlit as st

from services.api import get_dashboard

from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.cards import render_status_card
from utils.greetings import greeting

st.set_page_config(
    page_title="Database Driven LLM Wiki",
    page_icon="📚",
    layout="wide",
)


dashboard = get_dashboard()

render_sidebar(dashboard)

title, subtitle = greeting()

st.title(title)

st.caption(subtitle)

st.divider()

st.header("Database Driven LLM Wiki")

st.write(
    "Your AI-powered personal knowledge base."
)

st.divider()

render_metrics(dashboard)

st.divider()

# render_status_card(dashboard)

st.divider()

st.subheader("Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button(
        "💬 Ask Questions",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Ask_Questions.py")

with c2:
    if st.button(
        "📥 Ingest Documents",
        use_container_width=True,
    ):
        st.switch_page("pages/2_Ingest_Documents.py")

with c3:
    if st.button(
        "📚 Browse Wiki",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Browse_Wiki.py")