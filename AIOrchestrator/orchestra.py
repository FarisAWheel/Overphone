# The main file for the AI Orchestrator module
import os
import json
from sys import path

# Add the path to the parent directory
path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AdvanceAI.AdvanceAI import advance_generate_response
from tts.text_to_speech import text_to_speech
from Roberta.roberta import roberta_response

context_dict: dict[str, dict[str, list[str]]] = {}


def orchestrate(usrPrompt: str, caller_id):
    # If this is a new call, create the context for this caller
    if caller_id not in context_dict:
        context_dict[caller_id] = {"user": [], "assistant": []}

    # Adds the current user prompt to the context
    context_dict[caller_id]["user"].append(usrPrompt)

    response = advance_generate_response(context_dict[caller_id])

    try:
        # Remove the ```json and ``` from the response string
        response = response.replace("```json", "").replace("```", "").strip()
        response = json.loads(response)
        response = roberta_response(
            response["name"], response["pin"], response["question"]
        )

        print(response)

    except json.JSONDecodeError:
        pass

    # Store the new response as an assistant response in the context
    context_dict[caller_id]["assistant"].append(response)

    # Generates an audio file from the response to be used in the call
    return text_to_speech(response)


def delete_context_by_caller_id(caller_id):
    # Deletes the context for a specific caller
    del context_dict[caller_id]


if __name__ == "__main__":
    orchestrate(
        "My name is Alice and my pin is 1234 and I would like to check my balance",
        "4691234445",
    )
    orchestrate("What was my last question", "4691234445")
