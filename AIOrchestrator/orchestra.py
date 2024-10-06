# The main file for the AI Orchestrator module
import os
import json
from sys import path
import pathlib

# Add the path to the parent directory
path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AdvanceAI.AdvanceAI import advance_generate_response
from tts.text_to_speech import text_to_speech
from Roberta.roberta import roberta_response


context_dict: dict[str, dict[str, list[str]]] = {}

def load_preprompt(persona: str):
    preprompt = ""
    with open(str(pathlib.Path(__file__).parent.resolve()) + "/personas.json",'r') as file:
        personas_dict = json.load(file)
        preprompt = personas_dict["personas"][persona]["preprompt"]
    return preprompt


def orchestrate(usrPrompt: str, caller_id, persona: str):
    # If this is a new call, create the context for this caller
    if caller_id not in context_dict:
        context_dict[caller_id] = {"user": [], "assistant": [], "preprompt": load_preprompt(persona)}

    # Adds the current user prompt to the context
    context_dict[caller_id]["user"].append(usrPrompt)

    response = advance_generate_response(context_dict[caller_id])

    try:
        # Attempt to parse the response as JSON
        response_json = json.loads(response)
        if "goodbye" in response_json:
            # Ensure the directory exists
            os.makedirs("SignalWire/", exist_ok=True)
            # Write the goodbye message to a file
            with open(f"SignalWire/{caller_id}_goodbye.txt", "w") as file:
                file.write(response_json["goodbye"])
            return "CALL HAS ENDED"
        response = roberta_response(
            response_json["name"], response_json["pin"], response_json["question"]
        )
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
    except KeyError:
        print("JSON response does not contain expected keys.")

    print(response)

    # Store the new response as an assistant response in the context
    context_dict[caller_id]["assistant"].append(response)

    # Generates an audio file from the response to be used in the call
    return text_to_speech(response)


def delete_context_by_caller_id(caller_id):
    # Deletes the context for a specific caller
    del context_dict[caller_id]


if __name__ == "__main__":
    persona_input = input("Enter the persona you would like to use: ") 
    persona_input = persona_input.lower()
    orchestrate(
        "This is a pre-prompt that comes in when the User has succesfully connected, please welcome them accordingly especially according to the preprompt alreadys in system.",
        "4691234445",
        persona_input
    )
    user_prompt = ""
    while user_prompt.lower() != "goodbye":
        user_prompt = input("Enter your prompt: ") 
        orchestrate(
            user_prompt,
            "4691234445",
            persona_input
        )
