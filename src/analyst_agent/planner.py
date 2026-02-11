import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_plan(task: str, format: list[str]) -> list[str]:
    """
    Use an LLM to convert a task into a step-by-step plan.
    """

    prompt = f"""
        You are a task planner.

        Break the task into executable steps.

        IMPORTANT:
        - If external information is needed, output a step starting with:
        SEARCH: <query>

        - If a file needs to be read, output:
        READ_FILE: <filename>

        - If calculation is needed, output:
        CALCULATE: <expression>

        - Otherwise, output reasoning steps normally.

        Return the steps as a Python list.
        
        Task:
        {task}

        Constraint: You must structure your response using ONLY these exact headers: {format}.
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
        if line and len(line) > 1: #and line[0].isdigit()
            steps.append(line) #line.split(".", 1)[1].strip()

    if not steps:
        raise ValueError("Planner failed to produce steps")

    return steps


def is_plan_complete(state) -> bool:
    return state.current_step >= len(state.plan)
