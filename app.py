# app.py
import streamlit as st
from orchestrator import run_pipeline

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #F8FAFC;

    /* Green border effect */
    border: 3px solid #22c55e;
    box-shadow: 0 0 25px rgba(34,197,94,0.6);
    padding: 16px;
    border-radius: 18px;
}


h1, h2, h3 {
    color: #F8FAFC;
    font-weight: 700;
}

/* 🔥 FIX: input labels */
label {
    color: #F8FAFC !important;
    font-weight: 600;
}

textarea {
    border-radius: 14px !important;
    background-color: #0b1220 !important;
    color: #E5E7EB !important;
}


/* 🌟 Action buttons – yellow theme */
button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    color: #fde047 !important;              /* yellow text */
    border: 2px solid #fde047 !important;   /* yellow border */
    background: rgba(0,0,0,0.15) !important;
}

/* Hover effect */
button:hover {
    background: rgba(253,224,71,0.15) !important;
    box-shadow: 0 0 12px rgba(253,224,71,0.6);
}

/* Primary button (Build App) stays gradient */
button[kind="primary"] {
    background: linear-gradient(90deg, #22c55e, #16a34a) !important;
    color: #ffffff !important;
    border: none !important;
}


.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
}

.action-tile {
    background: rgba(255,255,255,0.12);
    padding: 16px;
    border-radius: 16px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Hero Section
# -------------------------------------------------
st.markdown("""
<div class="card">
    <h1>🧠 Agentic App Builder</h1>
    <p>
        Convert <b>natural language</b> into a <b>working application</b><br>
        using <span style="color:#A78BFA;">LLM-driven agent orchestration</span>.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Prompt Input
# -------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

user_prompt = st.text_area(
    "💬 Describe your app",
    height=150,
    placeholder=(
        "Example:\n"
        "Design a todo app.\n"
        "Add, list and delete tasks.\n"
        "Add button should be named ranit."
    )
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "context" not in st.session_state:
    st.session_state.context = {
        "idea": "",
        "intent": "",
        "features": [],
        "actions": {},
        "app_code": "",
        "issues": []
    }

# -------------------------------------------------
# Build Button (Centered)
# -------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    build_clicked = st.button("🚀 Build Application", type="primary")

if build_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a problem statement.")
    else:
        with st.status("🤖 Agents are working...", expanded=True) as status:

            def update_status(msg: str):
                status.write(f"⚙️ {msg}")

            st.session_state.context = run_pipeline(
                user_prompt,
                st.session_state.context,
                status_callback=update_status
            )

            status.update(
                label="✅ Application generated successfully!",
                state="complete"
            )

# -------------------------------------------------
# Render Generated App
# -------------------------------------------------
context = st.session_state.context

if context and context.get("app_code"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧩 Generated Application")
    st.markdown("</div>", unsafe_allow_html=True)

    local_scope = {"st": st}
    exec(context["app_code"], local_scope)

    item = st.text_input("Enter value")

    st.markdown("### ⚡ Actions")

    actions = context.get("actions", {})

    cols = st.columns(len(actions) if actions else 1)

    for col, (action, cfg) in zip(cols, actions.items()):
        if not cfg.get("enabled", True):
            continue

        label = cfg.get("label", action.capitalize())

        with col:
            st.markdown("<div class='action-tile'>", unsafe_allow_html=True)

            if action == "add":
                if st.button(label):
                    local_scope["add_item"](item)
                    st.success("Item added")

            elif action == "list":
                if st.button(label):
                    st.write(local_scope["list_items"]())

            elif action == "delete" and "delete_item" in local_scope:
                if st.button(label):
                    deleted = local_scope["delete_item"](item)
                    if deleted:
                        st.success("Item deleted")
                    else:
                        st.warning("Item not found")

            elif action == "clear_all" and "clear_all" in local_scope:
                if st.button(label):
                    local_scope["clear_all"]()
                    st.success("All tasks cleared")

            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------
    # Debug / Explainability
    # -------------------------------------------------
    with st.expander("🧠 Agent Reasoning & Context"):
        st.json(context)
