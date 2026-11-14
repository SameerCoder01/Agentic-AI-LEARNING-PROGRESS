
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import TypeAdapter, Field, ValidationError


# 1. Define Agent State

class AgentState(TypedDict):
    task: Annotated[str, Field(strict=True)]
    total_documents: Annotated[int, Field(strict=True)]
    completed_documents: Annotated[int, Field(strict=True)]
    pending_documents: Annotated[list[str], Field(strict=True)]
    status: Annotated[str, Field(strict=True)]


validator = TypeAdapter(AgentState)


# 2. Initial State

agent_state: AgentState = {
    "task": "Analyze research papers",
    "total_documents": 3,
    "completed_documents": 0,
    "pending_documents": [
        "paper1.pdf",
        "paper2.pdf",
        "paper3.pdf"
    ],
    "status": "pending"
}


# 3. Common State Update Function

def update_state(state, updates):

    updated_state = state.copy()
    updated_state.update(updates)

    try:
        validated_state = validator.validate_python(
            updated_state
        )

        state.update(validated_state)

        print("\nState updated successfully!")
        print(state)

    except ValidationError as error:
        print("\nState update failed!")
        print(error)


# 4. First PDF completed

print("\n--- PDF 1 COMPLETED ---")

update_state(agent_state, {
    "completed_documents": 1,
    "pending_documents": ["paper2.pdf", "paper3.pdf"],
    "status": "in_progress"
})


# 5. Second PDF completed

print("\n--- PDF 2 COMPLETED ---")

update_state(agent_state, {
    "completed_documents": 2,
    "pending_documents": ["paper3.pdf"],
    "status": "in_progress"
})

update_state(agent_state, {
    "completed_documents": "Hello",
    "status": "completed"
})

# 6. Third PDF completed

print("\n--- PDF 3 COMPLETED ---")

update_state(agent_state, {
    "completed_documents": 3,
    "pending_documents": [],
    "status": "completed"
})



# 7. Final State

print("\n--- FINAL AGENT STATE ---")
print(agent_state)
