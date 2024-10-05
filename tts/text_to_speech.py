from openai import OpenAI
import pathlib

def text_to_speech(text: str):
    client = OpenAI()
    stream_file_path: str = str(pathlib.Path(__file__).parent.resolve()) + "/audio_files/" + str(abs(hash(text))) + ".mp3"

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(stream_file_path)

if __name__ == "__main__":
    text_to_speech("Testing, testing, 1...2...3. AHHHHHHHHH TESTING TESTING DOES THIS WORK. IS THIS THING ON.");
    print(pathlib.Path(__file__).parent.resolve())
