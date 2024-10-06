import pathlib
import uuid
from deepgram import DeepgramClient, SpeakOptions

DEEPGRAM_API_KEY = "cb535db4ca226d274fab7b6631dcf43ebbf41159"

TEXT = {
    "text": "Deepgram is great for real-time conversations… and also, you can build apps for things like customer support, logistics, and more. What do you think of the voices?"
}
FILENAME = ""


def main():

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
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
