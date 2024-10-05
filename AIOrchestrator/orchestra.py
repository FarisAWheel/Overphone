# The main file for the AI Orchestrator module
from AdvanceAI import generate_response
from tts.text_to_speech import text_to_speech

def orchestrate(usrPrompt: str):
    response = generate_response(usrPrompt)

    # Genereates an audio file from the response to be used in the call
    return text_to_speech(response)
