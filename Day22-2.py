
from typing import Annotated, TYPE_CHECKING
from typing_extensions import TypedDict
from pydantic import TypeAdapter, Field, ValidationError


# =========================================
# 1. DEFINE STATE STRUCTURE
# =========================================

class AgentState(TypedDict):
    task: Annotated[str, Field(strict=True)]
    total_documents: Annotated[int, Field(strict=True)]
    completed_documents: Annotated[int, Field(strict=True)]
    status: Annotated[str, Field(strict=True)]


# Pydantic automatically reads this structure
state_validator = TypeAdapter(AgentState)


# =========================================
# 2. INITIAL STATE
# =========================================

agent_state: AgentState = {
    "task": "Compare research papers",
    "total_documents": 3,
    "completed_documents": 2,
    "status": "in_progress"
}

print("Initial State:")
print(agent_state)


# =========================================
# 3. AUTOMATIC RUNTIME VALIDATION
# =========================================

def update_state(state, field, new_value):

    # Create a copy so invalid changes don't affect original state
    updated_state = state.copy()

    # Change the requested field
    updated_state[field] = new_value

    try:
        # Validate complete state using Pydantic
        validated_state = state_validator.validate_python(
            updated_state
        )

        # Update original state only after successful validation
        state.update(validated_state)

        print(f"\n{field} updated successfully!")
        print(state)

    except ValidationError as error:

        print(f"\nValidation failed for field: {field}")
        print(error)


# =========================================
# 4. TEST INVALID UPDATES
# =========================================

print("\n--- TEST 1: Integer to String ---")

update_state(
    agent_state,
    "total_documents",
    "Hello"
)


print("\n--- TEST 2: String to Integer ---")

update_state(
    agent_state,
    "status",
    100
)


# =========================================
# 5. TEST VALID UPDATES
# =========================================

print("\n--- TEST 3: Valid Integer Update ---")

update_state(
    agent_state,
    "total_documents",
    5
)


print("\n--- TEST 4: Valid String Update ---")

update_state(
    agent_state,
    "status",
    "completed"
)


# =========================================
# 6. STATIC TYPE CHECKING DEMO
# =========================================

if TYPE_CHECKING:

    test_state: AgentState = {
        "task": "Research",
        "total_documents": "Hello",
        "completed_documents": 2,
        "status": "in_progress"
    }

    # Pyright / Mypy should report a type error
