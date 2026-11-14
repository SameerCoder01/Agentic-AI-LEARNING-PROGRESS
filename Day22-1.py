
from typing import TypedDict, List

class AgentState(TypedDict):
    task: str
    total_documents: int
    completed_documents: int
    pending_documents: List[str]
    status: str


agent_state: AgentState = {
    "task": "Compare research papers",
    "total_documents": 3,
    "completed_documents": 2,
    "pending_documents": ["paper3.pdf"],
    "status": "in_progress"
}

agent_state["completed_documents"] = 3
agent_state["pending_documents"] = []
agent_state["status"] = "completed"


agent_state["total_documents"] = "Hello"

print(agent_state)


print("Task:", agent_state["task"])
print("Total Documents:", agent_state["total_documents"])
print("Completed:", agent_state["completed_documents"])
print("Pending:", agent_state["pending_documents"])
print("Status:", agent_state["status"])
