# agents/architect.py

def architect_agent(context: dict) -> dict:
    """
    Architect Agent
    - Decides data model based on features
    - Keeps architecture minimal for MVP
    """

    features = context.get("features", [])

    # Simple single-entity data model
    if "add" in features or "list" in features:
        context["data_model"] = {
            "item": "string"
        }

    # App type (for future extension)
    context["app_type"] = "simple_list_app"

    return context
