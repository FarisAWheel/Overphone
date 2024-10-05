# The main file for the AI Orchestrator module
import os
import json
from sys import path

# Add the path to the parent directory
path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AdvanceAI.AdvanceAI import advance_generate_response
from tts.text_to_speech import text_to_speech
from Roberta.roberta import roberta_response

context_dict = {}

def orchestrate(usrPrompt: str, caller_id):
    response = advance_generate_response(usrPrompt)
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

    context_dict[caller_id] = { "user": usrPrompt, "assistant": response }

    # Generates an audio file from the response to be used in the call
    return text_to_speech(response)


if __name__ == "__main__":
    orchestrate(
        "Hi my name is Ballard Alice my pin is 1234 and I would like to know my account balance."
    )
