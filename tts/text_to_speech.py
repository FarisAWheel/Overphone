import pathlib
import azure.cognitiveservices.speech as speechsdk
import tempfile
import uuid


def text_to_speech(text: str):
    subscription_key = "cf799e65820748e798c0ec231f72f082"
    service_region = "eastus"

    filepath: str = (
        str(pathlib.Path(__file__).parent.resolve())
        + "/audio_files/"
        + str(uuid.uuid4())
        + ".mp3"
    )

    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key,
        region=service_region,
    )
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
    temp_file_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    text_to_speak = text
    result = speech_synthesizer.speak_text_async(text_to_speak).get()

    return filepath


def delete_audio_file(file_path: str):
    try:
        pathlib.Path(file_path).unlink()
    except:
        return -1


if __name__ == "__main__":
    print(text_to_speech("This is a test of the text to speech function."))
    print(pathlib.Path(__file__).parent.resolve())
