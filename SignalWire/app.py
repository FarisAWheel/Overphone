

import os
import sys

# Add the directory containing AIOrchestrator to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pathlib
from flask import Flask, request, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime
from AIOrchestrator.orchestra import orchestrate, delete_context_by_caller_id
from tts.text_to_speech import delete_audio_file
from tts.text_to_speech import text_to_speech
import time

app = Flask(__name__)



# Handles any incoming calls to the server and welcomes the caller
@app.route("/", methods=["GET", "POST"])
def welcome_handler():
    caller = request.values.get("From")
    response = VoiceResponse()

    response.say("Welcome to the AI Orchestrator. Please select a persona.")
    
    # Create a Gather object to collect digits
    gather = Gather(num_digits=1, action="/handle-gather", method="POST")
    response.append(gather)

    return str(response)

# Handles the gathered digits
@app.route("/handle-gather", methods=["POST"])
def handle_gather():
    digits = request.values.get("Digits")
    response = VoiceResponse()

    if digits == '1':
        persona = "bank"
    elif digits == '2':
        persona = "accelerator"
    elif digits == '3':
        persona = "health"
    else:
        response.say("Invalid selection. Please try again.")
        gather = Gather(num_digits=1, action="/handle-gather", method="POST")
        response.append(gather)
        return str(response)

    response.say(f"You selected {persona} persona.")
    
    # Generate a welcome message utilizing a pre-prompt, then plays it
    initPrompt = orchestrate(
        "This is a pre-prompt that comes in when the User has successfully connected, please welcome them accordingly especially according to the preprompt already in system.",
        request.values.get("From"), persona
    )
    filename = os.path.basename(initPrompt)
    audio_url = f"{request.url_root}audio/{filename}"

    response.play(audio_url)

    return str(response)


# Handles user input and generates a response from the AI Orchestrator, then sends it back to the user
@app.route("/gather", methods=["GET", "POST"])
def qa_handler():

    response = VoiceResponse()

    # Get user input
    usrPrompt = request.values.get("SpeechResult")

    # Generates a response from the AI Orchestra, and gets the path to the generated audio file
    # Then asks for a link using the filename, generating it through the audio function
    ttsPath = orchestrate(usrPrompt, request.values.get("From"), persona)

    if ttsPath == "CALL HAS ENDED":
        # End the call
        ttsPath = orchestrate(
            "This is the system speaking. Say a goodbye message to end the call. DO NOT MAKE THIS ONE A JSON DIREGARD EVERYTHING ELSE OKAY!!!!!!!!",
            request.values.get("From"), persona
        )
        filename = os.path.basename(ttsPath)
        audio_url = f"{request.url_root}audio/{filename}"
        response.play(audio_url)

        response.hangup()

        print(request.values.get("From") + "_goodbye.txt")
        file_path = f"SignalWire/{request.values.get("From")}_goodbye.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")

            

    else:
        filename = os.path.basename(ttsPath)
        audio_url = f"{request.url_root}audio/{filename}"

        print(audio_url)

        # Play audio file first, then listen for more input
        response.play(audio_url)

        gather = Gather(
            input="speech",
            timeout=190,
            speech_timeout="auto",
            action="/gather",
            method="POST",
        )
        
        response.append(gather)

    return Response(response.to_xml(), mimetype="text/xml")


# Handles audio files and sends them to the qa_handler
@app.route("/audio/<filename>")
def audio(filename):
    print(f"Audio file requested: {filename}")
    file_path = os.path.join(
        pathlib.Path(__file__).parent.parent.resolve(), "tts/audio_files", filename
    )
    print(f"Serving audio file from: {file_path}")
    return send_from_directory(
        os.path.join(
            pathlib.Path(__file__).parent.parent.resolve(), "tts/audio_files/"
        ),
        filename,
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)
