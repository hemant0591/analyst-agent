import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def llm_reason(step: str, context: list[str]) -> str:
    """
    Use the LLM to reason about a single step.
    """

    prompt = f"""
        You are an analytical assistant.

        Current task step:
        {step}

        Previous observations:
        {context}

        Provide a concise, factual analysis for this step.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def calculate(expression: str) -> str:
    """
    Safely evaluate simple arithmetic expressions.
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"


def execute_step(step: str, observations: list[str]) -> str:
    step_lower = step.lower()

    # Heuristic routing (simple, transparent)
    if "calculate" in step_lower or "estimate" in step_lower:
        return calculate(step)

    # Default: reasoning step
    return llm_reason(step, observations)