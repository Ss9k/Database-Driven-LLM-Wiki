import streamlit as st

from services.api import health

st.set_page_config(
    page_title="Health Report",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Wiki Health Report")

st.caption(
    "Monitor the health of your knowledge base."
)

# --------------------------------------------------
# Load Health Report
# --------------------------------------------------

data = health()

broken_links = data.get("broken_links", [])

orphan_pages = data.get("orphan_pages", [])

duplicate_pages = data.get("duplicate_pages", [])

# --------------------------------------------------
# Summary Cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🔗 Broken Links",
        len(broken_links)
    )

with col2:

    st.metric(
        "📄 Orphan Pages",
        len(orphan_pages)
    )

with col3:

    st.metric(
        "🧬 Duplicate Pages",
        len(duplicate_pages)
    )

st.divider()

# --------------------------------------------------
# Overall Health
# --------------------------------------------------

total_issues = (
    len(broken_links)
    + len(orphan_pages)
    + len(duplicate_pages)
)

if total_issues == 0:

    st.success(
        "🎉 Your knowledge base is healthy."
    )

else:

    st.warning(
        f"⚠️ {total_issues} issue(s) detected."
    )

# --------------------------------------------------
# Broken Links
# --------------------------------------------------

with st.expander(
    f"🔗 Broken Links ({len(broken_links)})",
    expanded=False,
):

    if not broken_links:

        st.success(
            "No broken links found."
        )

    else:

        for item in broken_links:

            st.markdown(
                f"""
**Page**

`{item['page']}`

Broken Link

`{item['broken_link']}`
"""
            )

            st.divider()

# --------------------------------------------------
# Orphan Pages
# --------------------------------------------------

with st.expander(
    f"📄 Orphan Pages ({len(orphan_pages)})",
    expanded=False,
):

    if not orphan_pages:

        st.success(
            "No orphan pages found."
        )

    else:

        for page in orphan_pages:

            st.markdown(
                f"• **{page}**"
            )

# --------------------------------------------------
# Duplicate Pages
# --------------------------------------------------

with st.expander(
    f"🧬 Duplicate Pages ({len(duplicate_pages)})",
    expanded=False,
):

    if not duplicate_pages:

        st.success(
            "No duplicate pages found."
        )

    else:

        for item in duplicate_pages:

            st.markdown(
                f"""
**{item['page1']}**

↔

**{item['page2']}**

Similarity

`{item['score']:.3f}`
"""
            )

            st.divider()

# --------------------------------------------------
# Refresh
# --------------------------------------------------

st.divider()

if st.button(
    "🔄 Refresh Report",
    use_container_width=True,
):

    st.rerun()