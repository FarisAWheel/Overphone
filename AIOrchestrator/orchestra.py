# the main file for the AI Orchestrator module

from analyzer import isComplex
from advanced_gpt.generate_response import generate_response

def orchestrate(usrPrompt: str):
    response = ""
    if isComplex(usrPrompt):
        response = generate_response(usrPrompt)
    else:
        print("GPT 2 is not setup yet, utiilizing GPT 4...")
        response = generate_response(usrPrompt)

      


