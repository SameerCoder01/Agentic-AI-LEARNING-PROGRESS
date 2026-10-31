
# DAY 19-2: MULTIPLE TOOL CALLING
# ERROR HANDLING AND RETRY MECHANISM


# STEP 1: IMPORT LIBRARIES

import json
import os

from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


# STEP 2: LOAD API KEY FROM .env

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        f"GROQ_API_KEY missing or empty. Check: {env_path}"
    )


# STEP 3: INITIALIZE GROQ CLIENT

groq_client = Groq(api_key=api_key)

GROQ_MODEL = "openai/gpt-oss-120b"


# STEP 4: DEFINE PYTHON FUNCTIONS

def calculate_percentage(number, percentage):

    return number * percentage / 100


def calculate_sum(a, b):

    return a + b


# STEP 5: CREATE TOOL REGISTRY

tool_registry = {
    "calculate_percentage": calculate_percentage,
    "calculate_sum": calculate_sum,
}


# STEP 6: DEFINE TOOL SCHEMAS

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_percentage",
            "description": "Calculate a percentage of a number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "number"},
                    "percentage": {"type": "number"},
                },
                "required": ["number", "percentage"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Calculate the sum of two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
]


# STEP 7: GET USER QUERY

user_query = (
    "Perform these TWO independent calculations:\n"
    "1. Calculate 10% of 200.\n"
    "2. Calculate 20% of 500.\n\n"
    "Use calculate_percentage for both calculations."
)


messages = [
    {
        "role": "system",
        "content": (
            "You are a calculator assistant. "
            "You MUST use Python tools for all calculations. "
            "When multiple independent calculations are requested, "
            "request all corresponding tool calls in the same response "
            "if possible. "
            "If a tool returns an execution error, understand the error "
            "and retry with corrected arguments. "
            "Do not repeat the same invalid arguments."
        ),
    },
    {
        "role": "user",
        "content": user_query,
    },
]


# STEP 8: ITERATIVE TOOL CALLING

max_iterations = 10
max_tool_retries = 3

iteration = 0
tool_errors = 0

final_answer_received = False
stop_execution = False


while iteration < max_iterations:

    if stop_execution:
        break

    iteration += 1

    print(f"\n--- Iteration {iteration} ---")

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=True,
        temperature=0,
    )

    message = response.choices[0].message

    print(
        "Finish reason:",
        response.choices[0].finish_reason
    )


    # CASE 1: NO TOOL CALLS

    if not message.tool_calls:

        final_answer = message.content

        print("\nFinal Answer:", final_answer)

        final_answer_received = True

        break


    # CASE 2: MODEL REQUESTED TOOL CALLS

    print(
        "\nNumber of tool calls:",
        len(message.tool_calls)
    )


    # ADD ASSISTANT TOOL-CALL MESSAGE TO HISTORY

    messages.append({
        "role": "assistant",
        "content": message.content,
        "tool_calls": [
            {
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                },
            }
            for call in message.tool_calls
        ],
    })


    # EXECUTE EVERY REQUESTED TOOL

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        print("\nTool name:", tool_name)

        try:

            # Parse tool arguments.

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Find the corresponding Python function.

            function_to_call = tool_registry.get(tool_name)

            if function_to_call is None:

                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )

            # Execute the function.

            result = function_to_call(**arguments)

            print("Tool result:", result)

            # Reset consecutive error counter after success.
            tool_errors = 0

            tool_response = {
                "status": "success",
                "result": result
            }


        except (json.JSONDecodeError, TypeError, ValueError, KeyError) as error:

            # Handle tool execution failure.

            tool_errors += 1

            print("Tool execution failed:", error)

            print(
                f"Retry attempts used: {tool_errors}/{max_tool_retries}"
            )

            tool_response = {
                "status": "error",
                "error": str(error),
                "instruction": (
                    "Correct the tool arguments and retry."
                )
            }


        # SEND RESULT OR ERROR BACK TO THE MODEL.

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_response)
        })


        # STOP AFTER MAXIMUM FAILED ATTEMPTS.

        if tool_errors >= max_tool_retries:

            print("\nMaximum tool retry limit reached.")

            stop_execution = True

            break


# STEP 9: HANDLE MAXIMUM ITERATIONS OR RETRY LIMIT

if not final_answer_received:

    if stop_execution:

        print(
            "\nAgent stopped because maximum tool retries were reached."
        )

    else:

        print("\nMaximum iterations reached.")

        print("Requesting final response...")

        final_response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tool_choice="none",
        )

        final_answer = final_response.choices[0].message.content

        if final_answer:

            print("\nFinal Answer:", final_answer)

        else:

            print("\nNo final answer was returned.")
