from openai import OpenAI
import pathlib


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
        return stream_file_path
    except:
        return -1


def delete_audio_file(file_path: str):
    try:
        pathlib.Path(file_path).unlink()
    except:
        return -1


if __name__ == "__main__":
    text_to_speech(
        """
        There are several types of bank accounts, each serving different purposes. Here are some common types:

        1. **Checking Account**: This account is used for everyday transactions, such as deposits, withdrawals, and bill payments. It typically offers easy access to funds through checks, debit cards, and ATMs.

        2. **Savings Account**: This account is designed for saving money and usually earns interest. Access to funds is limited to encourage saving.

        3. **Money Market Account**: A hybrid between checking and savings accounts, this account usually offers higher interest rates but may require a higher minimum balance.

        4. **Certificate of Deposit (CD)**: This is a time-bound savings account that offers higher interest rates but requires you to lock in your money for a specific term.

        5. **Retirement Accounts**: These accounts, like IRAs or 401(k)s, are designed for long-term savings for retirement and often come with tax advantages.

        If you have specific questions about any account type or need more details, feel free to ask!
        """
    )
    print(pathlib.Path(__file__).parent.resolve())
