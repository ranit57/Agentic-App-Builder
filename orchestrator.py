# orchestrator.py

from agents.planner import planner_agent
from agents.architect import architect_agent
from agents.coder import code_agent
from agents.reviewer import reviewer_agent


def run_pipeline(user_input: str, context: dict, status_callback=None) -> dict:
    """
    State-aware, intent-aware orchestration pipeline
    """

    # ---------------- Planner ----------------
    if status_callback:
        status_callback("Planner Agent: understanding intent and features...")
    context = planner_agent(user_input, context)

    intent = context.get("intent")

    # ---------------- Orchestration ----------------
    if intent == "new_app":
        if status_callback:
            status_callback("Architect Agent: designing app structure...")
        context = architect_agent(context)

        if status_callback:
            status_callback("Code Agent: generating application logic...")
        context = code_agent(context)

    elif intent == "feature_update":
        if status_callback:
            status_callback("Code Agent: updating application logic...")
        context = code_agent(context)

    elif intent == "bug_fix":
        # Ensure code exists
        if not context.get("app_code"):
            if status_callback:
                status_callback("Code Agent: ensuring base logic exists...")
            context = code_agent(context)

    # Reviewer always runs
    if status_callback:
        status_callback("Reviewer Agent: validating and refining...")
    context = reviewer_agent(context)

    if status_callback:
        status_callback("Pipeline completed")

    return context
