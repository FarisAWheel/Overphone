from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def call_handler():
    """
    This endpoint will be queried by SignalWire whenever an incoming call is received.
    We respond with an XML document which specifies the next instructions.
    """
    print(request.values)

    # Get the caller's number
    caller = request.values.get('From')

    now = datetime.now()

    response = VoiceResponse()
    response.say(f"Welcome! Today is {now.strftime('%A')}.")
    response.say(f"Your phone number ends in {caller[-2:]}.")
    if now.weekday() >= 5:
        response.say(f"Enjoy the weekend.")

    return Response(response.to_xml(), mimetype='text/xml')

if __name__ == "__main__":
    app.run(port=5000)