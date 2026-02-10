import yaml
from pathlib import Path

from analyst_agent.memory import AgentState
from analyst_agent.planner import create_plan, is_plan_complete
from analyst_agent.tools import execute_step

def load_task_from_yaml(path: str) -> str:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["task"]

def run_agent(task: str | None = None, config_path: str = "config/task.yaml") -> AgentState:
    if task is None:
        task = load_task_from_yaml(config_path)

    state = AgentState(task=task)

    print("=== AGENT START ===")
    print(f"Task: {state.task}\n")

    while not state.done:
        # Phase 1: Planning
        if not state.plan:
            print("Planning...")
            state.plan = create_plan(state.task)
            print(f"Plan created: {state.plan}\n")
            continue

        # Phase 2: Execution
        if not is_plan_complete(state):
            step = state.plan[state.current_step]
            print(f"Executing step {state.current_step + 1}: {step}")

            result = execute_step(step, state.observations)
            state.observations.append(result)

            print(f"Observation: {result}\n")
            state.current_step += 1
            continue

        # Phase 3: Termination
        print("All steps completed. Finalizing output...\n")
        state.final_output = {
            "task": state.task,
            "steps": state.plan,
            "observations": state.observations,
        }
        state.done = True

    print("=== AGENT END ===\n")
    return state
