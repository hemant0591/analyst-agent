import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_plan(task: str) -> list[str]:
    """
    Use an LLM to convert a task into a step-by-step plan.
    """

    prompt = f"""
        You are a planning assistant.

        Given a task, produce a clear step-by-step plan.
        Each step should be short and actionable.

        Return ONLY a numbered list of steps.
        Do not include explanations.

        Task:
        {task}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    text = response.choices[0].message.content.strip()

    # Parse numbered list safely
    steps = []
    for line in text.splitlines():
        line = line.strip()
        if line and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    if not steps:
        raise ValueError("Planner failed to produce steps")

    return steps


def is_plan_complete(state) -> bool:
    return state.current_step >= len(state.plan)
