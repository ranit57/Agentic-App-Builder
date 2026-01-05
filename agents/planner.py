# agents/planner.py

import subprocess
import json
import textwrap
import time

# -------------------------------------------------
# LLM Call (Safe)
# -------------------------------------------------
def call_llm(prompt: str, retries=1, timeout=30) -> dict:
    """
    Safe LLM call with timeout, retry, and fallback
    """
    for attempt in range(retries + 1):
        try:
            process = subprocess.run(
                ["ollama", "run", "mistral"],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )

            output = process.stdout.decode("utf-8", errors="ignore").strip()
            return json.loads(output)

        except subprocess.TimeoutExpired:
            print(f"[Planner] LLM timeout (attempt {attempt + 1})")
            time.sleep(1)

        except Exception as e:
            print("[Planner] LLM error:", e)
            break

    # -------- HARD FALLBACK --------
    return {
        "intent": "new_app",
        "features": ["add", "list", "delete"],
        "actions": {
            "add": {"label": "Add", "enabled": True},
            "list": {"label": "List", "enabled": True},
            "delete": {"label": "Delete", "enabled": True}
        },
        "_degraded": True
    }


# -------------------------------------------------
# Validation Layer
# -------------------------------------------------
def normalize_actions(raw_actions: dict) -> dict:
    safe_actions = {}

    for action, cfg in raw_actions.items():
        if not isinstance(cfg, dict):
            continue

        label = cfg.get("label", action.capitalize())
        enabled = cfg.get("enabled", True)

        if not isinstance(label, str):
            label = action.capitalize()
        if not isinstance(enabled, bool):
            enabled = True

        safe_actions[action] = {
            "label": label,
            "enabled": enabled
        }

    return safe_actions


# -------------------------------------------------
# Context Memory Helpers
# -------------------------------------------------
def update_context_memory(context: dict, user_input: str, max_len=5):
    memory = context.get("context_memory", [])
    memory.append(user_input)

    # Keep only last N prompts
    context["context_memory"] = memory[-max_len:]


def build_context_summary(context: dict) -> str:
    memory = context.get("context_memory", [])
    actions = context.get("actions", {})
    features = context.get("features", [])

    enabled_actions = [
        f"{k} ({v.get('label')})"
        for k, v in actions.items()
        if v.get("enabled", True)
    ]

    return f"""
Previous user instructions (latest last):
{memory}

Current application state:
- Features: {features}
- Enabled actions: {enabled_actions}
"""


# -------------------------------------------------
# Planner Agent (Context-Aware)
# -------------------------------------------------
def planner_agent(user_input: str, context: dict) -> dict:
    """
    LLM-based, context-aware Planner Agent
    """

    # ---- Update memory first ----
    update_context_memory(context, user_input)

    context_summary = build_context_summary(context)

    prompt = textwrap.dedent(f"""
    You are a planner agent in an agentic app builder.

    IMPORTANT:
    The user may be CONTINUING or MODIFYING an existing app.
    Use the previous context carefully.

    {context_summary}

    Analyze the NEW user request and extract:

    1. intent: one of ["new_app", "feature_update", "bug_fix"]
    2. features: list of logical capabilities (add, list, delete, clear_all, etc.)
    3. actions: UI actions with label and enabled flag

    Rules:
    - Respond ONLY in valid JSON
    - No explanations
    - Modify the existing app incrementally
    - Do NOT repeat unchanged actions
    - If user disables a button, set enabled=false

    Example output:
    {{
      "intent": "feature_update",
      "features": ["add", "list", "delete"],
      "actions": {{
        "delete": {{ "label": "remove_task", "enabled": true }}
      }}
    }}

    User request:
    {user_input}
    """)

    result = call_llm(prompt)

    # ---- Merge with existing context ----
    prev_actions = context.get("actions", {})
    raw_actions = result.get("actions", prev_actions)

    context["idea"] = user_input
    context["intent"] = result.get("intent", context.get("intent", "new_app"))
    context["features"] = result.get("features", context.get("features", []))
    context["actions"] = normalize_actions({**prev_actions, **raw_actions})

    # ---- Mark degraded mode ----
    if result.get("_degraded"):
        context.setdefault("issues", []).append(
            "LLM timeout – fallback planner used"
        )

    return context
