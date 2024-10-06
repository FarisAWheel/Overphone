import sys
import os
import pathlib

# Add the directory containing AIOrchestrator to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime
from AIOrchestrator.orchestra import orchestrate, delete_context_by_caller_id
from tts.text_to_speech import delete_audio_file
from tts.text_to_speech import text_to_speech

app = Flask(__name__)


# Handles any incoming calls to the server and welcomes the caller
@app.route("/", methods=["GET", "POST"])
def welcome_handler():
    # The endpoint will be queried by SignalWire when calls are received
    # The request will be responded to with an XML document, generated by the AI Orchestrator

    # Get called number and time
    caller = request.values.get("From")

    # Generate a test response (Will be replaced by AI Orchestrator)
    response = VoiceResponse()

    # Genereates a welcome message utilizing a pre-prompt, then plays it
    initPrompt = orchestrate(
        "This is a pre-prompt that comes in when the User has succesfully connected, please welcome them accordingly especially according to the preprompt alreadys in system.",
        caller,
    )
    filename = os.path.basename(initPrompt)
    audio_url = f"{request.url_root}audio/{filename}"

    response.play(audio_url)

    # Redirects to the gather endpoint to get user input
    gather = Gather(
        input="speech",
        timeout=30,
        speech_timeout="auto",
        action="/gather",
        method="POST",
    )

    response.append(gather)

    return Response(response.to_xml(), mimetype="text/xml")


# Handles user input and generates a response from the AI Orchestrator, then sends it back to the user
@app.route("/gather", methods=["GET", "POST"])
def qa_handler():

    response = VoiceResponse()

    caller_id = request.values.get("From")
    goodbye_file_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        f"{caller_id}_goodbye.txt",
    )
    print(os.path.exists(goodbye_file_path))
    if os.path.exists(goodbye_file_path):
        with open(goodbye_file_path, "r") as file:
            goodbye_message = file.read()
            ttsPath = text_to_speech(goodbye_message)
            print(ttsPath)
            filename = os.path.basename(ttsPath)
            print(filename)
            audio_url = f"{request.url_root}audio/{filename}"

            response.play(audio_url)

            response.hangup()
            delete_context_by_caller_id(caller_id)
            os.remove(goodbye_file_path)

    else:

        # Get user input
        usrPrompt = request.values.get("SpeechResult")

        # Generates a response from the AI Orchestra, and gets the path to the generated audio file
        # Then asks for a link using the filename, generating it through the audio function
        ttsPath = orchestrate(usrPrompt, request.values.get("From"))

        if ttsPath != "CALL HAS ENDED":

            filename = os.path.basename(ttsPath)
            audio_url = f"{request.url_root}audio/{filename}"

            # Play audio file first, then listen for more input
            # response.play(audio_url)

            gather = Gather(
                input="speech",
                timeout=30,
                speech_timeout="auto",
                action="/gather",
                method="POST",
            )
            gather.play(audio_url)
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
