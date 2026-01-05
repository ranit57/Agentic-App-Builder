# # llm/local_llm.py

import subprocess
import json
import textwrap

def call_local_llm(user_input: str) -> dict:
    prompt = textwrap.dedent(f"""
    You are a planner agent.

    Extract the following from the user request:
    - features: list of actions (add, list, delete)
    - app_type: short string

    Respond ONLY in valid JSON.
    No explanation. No markdown.

    User request:
    {user_input}
    """)

    try:
        process = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),   # 👈 key fix
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        output = process.stdout.decode("utf-8", errors="ignore").strip()

        return json.loads(output)

    except Exception as e:
        print("LLM error:", e)

        # Safe fallback (MVP never breaks)
        return {
            "features": ["add", "list"],
            "app_type": "simple_list_app"
        }
