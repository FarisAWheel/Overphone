# The main file for the AI Orchestrator module
import sys
import os

# Add the directory containing AdvanceAI to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AdvanceAI')))

from AdvanceAI import advance_generate_response
from tts.text_to_speech import text_to_speech

def orchestrate(usrPrompt: str):
    response = advance_generate_response(usrPrompt)

    # Genereates an audio file from the response to be used in the call
    return text_to_speech(response)
