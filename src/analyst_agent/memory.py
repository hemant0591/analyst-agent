from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class AgentState:
    task: str
    plan: List[str] = field(default_factory=list)
    current_step: int = 0
    observations: List[Any] = field(default_factory=list)
    final_output: Any = None
    done: bool = False