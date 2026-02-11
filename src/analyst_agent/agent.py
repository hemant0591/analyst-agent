import yaml
from pathlib import Path

from analyst_agent.coordinator import Coordinator
from analyst_agent.memory import AgentMemory
from analyst_agent.planner import create_plan #, is_plan_complete
from analyst_agent.tools import execute_step

def load_task_from_yaml(path: str) -> str:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["task"]


def run_agent(task: str | None = None, config_path: str = "config/task.yaml"):
    if task is None:
        task = load_task_from_yaml(config_path)

    coordinator = Coordinator()
    memory = coordinator.run(task)

    print("\n===== FINAL SUMMARY =====\n")
    print(memory.final_output)
    return memory
