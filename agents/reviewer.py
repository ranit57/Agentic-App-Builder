# agents/reviewer.py
def reviewer_agent(context: dict) -> dict:
    """
    Reviewer Agent
    - Improves robustness
    - Handles common edge cases
    - Enables iterative enhancement
    """

    code = context.get("app_code", "")

    improvements = []

    # Ensure list_items always returns a copy (safe)
    if "def list_items" in code and "return items.copy()" not in code:
        improvements.append(
            code.replace("return items", "return items.copy()")
        )

    # Add fallback delete if mentioned but missing
    if "delete" in context["features"] and "def delete_item" not in code:
        improvements.append(
            code + """

def delete_item(item):
    if item in items:
        items.remove(item)
"""
        )

    # Apply latest improvement if any
    if improvements:
        context["app_code"] = improvements[-1]

    return context
