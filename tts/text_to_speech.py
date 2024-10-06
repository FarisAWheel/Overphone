import pathlib
import uuid
from deepgram import DeepgramClient, SpeakOptions

DEEPGRAM_API_KEY = "cb535db4ca226d274fab7b6631dcf43ebbf41159"

TEXT = {
    "text": "Deepgram is great for real-time conversations… and also, you can build apps for things like customer support, logistics, and more. What do you think of the voices?"
}
FILENAME = ""


def text_to_speech(text: str):
    FILENAME: str = (
        str(pathlib.Path(__file__).parent.resolve())
        + "/audio_files/"
        + str(uuid.uuid4())
        + ".mp3"
    )

    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        options = SpeakOptions(
            model="aura-asteria-en",
        )

        response = deepgram.speak.v("1").save(FILENAME, TEXT, options)

    except Exception as e:
        print(f"Exception: {e}")

    return FILENAME


def delete_audio_file(file_path: str):
    try:
        pathlib.Path(file_path).unlink()
    except:
        return -1


if __name__ == "__main__":
    print(text_to_speech("This is a test of the text to speech function."))
    print(pathlib.Path(__file__).parent.resolve())
