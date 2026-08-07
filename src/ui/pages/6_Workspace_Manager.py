import streamlit as st

from services.api import (
    projects,
    switch_project,
    delete_project,
    create_project,
)

st.set_page_config(
    page_title="Workspace Manager",
    page_icon="🗂",
    layout="wide",
)

st.title("🗂 Workspace Manager")

st.caption(
    "Manage independent knowledge base workspaces."
)

# ---------------------------------------
# Load Projects
# ---------------------------------------

response = projects()

projects = response.get(
    "projects",
    []
)

# =======================================
# Create Project
# =======================================

st.subheader("➕ Create Project")

new_project = st.text_input(
    "Project Name",
    placeholder="Quantum Wiki"
)

if st.button(
    "Create Project",
    use_container_width=True
):

    if not new_project.strip():

        st.warning(
            "Enter project name."
        )

    else:

        result = create_project(
            new_project
        )

        if result.get("status") == "success":

            st.success(
                result.get("message")
            )

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Failed."
                )
            )

st.divider()

# =======================================
# Switch Project
# =======================================

st.subheader("🔄 Switch Workspace")

selected = st.selectbox(
    "Available Projects",
    projects
)

if st.button(
    "Switch Workspace",
    use_container_width=True
):

    result = switch_project(
        selected
    )

    if result.get("status") == "success":

        st.success(
            result.get("message")
        )

    else:

        st.error(
            result.get(
                "message",
                "Unable to switch."
            )
        )

st.divider()

# =======================================
# Delete Project
# =======================================

st.subheader("🗑 Delete Workspace")

delete_target = st.selectbox(
    "Workspace",
    projects,
    key="delete"
)

confirm = st.checkbox(
    "I understand this action cannot be undone."
)

if st.button(
    "Delete Workspace",
    use_container_width=True,
    type="primary"
):

    if not confirm:

        st.warning(
            "Please confirm deletion."
        )

    else:

        result = delete_project(
            delete_target
        )

        if result.get("status") == "success":

            st.success(
                result.get("message")
            )

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Deletion failed."
                )
            )

st.divider()

# =======================================
# Existing Workspaces
# =======================================

st.subheader("📂 Existing Workspaces")

if not projects:

    st.info(
        "No workspaces found."
    )

else:

    for project in projects:

        st.markdown(
            f"📁 **{project}**"
        )