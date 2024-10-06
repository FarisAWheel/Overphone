from openai import OpenAI
import pathlib
# PYDUB USES FFMPEG BACKEND, PLEASE INSTALL FFMPEG
# LINUX: sudo apt-get install ffmpeg
# WINDOWS: https://www.wikihow.com/Install-FFmpeg-on-Windows
# MAC: brew install ffmpeg
from pydub import AudioSegment
from pydub.utils import which

#ensure that ffmpeg is set up
ffmpeg_path = which("ffmpeg")
if not ffmpeg_path:
    raise Exception("ffmpeg not found. Install ffmpeg to use this feature.")

def text_to_speech(text: str):
    client = OpenAI()
    stream_file_path: str = (
        str(pathlib.Path(__file__).parent.resolve())
        + "/audio_files/"
        + str(abs(hash(text)))
        + ".mp3"
    )

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    try:
        response.stream_to_file(stream_file_path)

        # Increase volume of mp3
        # Increase volume using pydub with simpleaudio backend
        audio = AudioSegment.from_file(stream_file_path)
        louder_audio = audio + 10  # Increase volume by 10dB
        louder_audio.export(stream_file_path, format="mp3")


        return stream_file_path
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return -1


if __name__ == "__main__":
    text_to_speech(
        "Testing, testing, 1...2...3. AHHHHHHHHH TESTING TESTING DOES THIS WORK. IS THIS THING ON."
    )
    print(pathlib.Path(__file__).parent.resolve())
