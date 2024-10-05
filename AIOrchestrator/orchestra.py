# The main file for the AI Orchestrator module
import os
import json
from sys import path

# Add the path to the parent directory
path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AdvanceAI.AdvanceAI import advance_generate_response
from tts.text_to_speech import text_to_speech
from Roberta.roberta import roberta_response


def orchestrate(usrPrompt: str):
    response = advance_generate_response(usrPrompt)
    try:
        # Remove the ```json and ``` from the response string
        response = response.replace("```json", "").replace("```", "").strip()
        response = json.loads(response)
        response = roberta_response(
            response["name"], response["pin"], response["question"]
        )

        # Extract the text response from the dictionary
        response = response.get("answer", "")
    except json.JSONDecodeError:
        pass

    # Generates an audio file from the response to be used in the call
    return text_to_speech(response)


if __name__ == "__main__":
    orchestrate("What did you hear me know")
