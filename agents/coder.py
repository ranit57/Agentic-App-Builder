# agents/coder.py

def code_agent(context: dict) -> dict:
    """
    Code Agent
    Generates Streamlit-safe application logic based on features
    """

    features = context.get("features", [])

    code_lines = [
        # ---------------- State ----------------
        "def get_items():",
        "    if 'items' not in st.session_state:",
        "        st.session_state['items'] = []",
        "    return st.session_state['items']",
        "",
        # ---------------- Add ----------------
        "def add_item(item):",
        "    if item:",
        "        get_items().append(item)",
        "",
        # ---------------- List ----------------
        "def list_items():",
        "    return get_items().copy()",
        ""
    ]

    # ---------------- Delete ----------------
    if "delete" in features:
        code_lines.extend([
            "def delete_item(item):",
            "    items = get_items()",
            "    original_len = len(items)",
            "    items[:] = [i for i in items if i != item]",
            "    return len(items) < original_len",
            ""
        ])

    # ---------------- Clear All (Optional) ----------------
    if "clear_all" in features:
        code_lines.extend([
            "def clear_all():",
            "    get_items().clear()",
            ""
        ])

    context["app_code"] = "\n".join(code_lines)
    return context
