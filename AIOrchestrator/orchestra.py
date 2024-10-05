# The main file for the AI Orchestrator module
from AdvanceAI.AdvanceAi import advance_generate_response
from tts.text_to_speech import text_to_speech
from Roberta.roberta import roberta_response


def orchestrate(usrPrompt: str):
    response = advance_generate_response(usrPrompt)

    # Genereates an audio file from the response to be used in the call
    return text_to_speech(response)
    response = advance_generate_response(usrPrompt)
    try:
        # Remove the ```json and ``` from the response string
        response = response.replace("```json", "").replace("```", "").strip()
        response = json.loads(response)
        response = roberta_response(
            response["name"], response["pin"], response["question"]
        )
    except json.JSONDecodeError:
        pass

    # Generates an audio file from the response to be used in the call
    return text_to_speech(response)


if __name__ == "__main__":
    orchestrate(
        "Hi! How much money do I have in my checking account? My name is Alice and my PIN is 1234."
    )
