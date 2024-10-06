import os
import json
from sys import path

from openai import OpenAI  # type: ignore


def advance_generate_response(context):
    print("user = " + str(context["user"]))
    print("assistant = " + str(context["assistant"]))
    client = OpenAI()
    preprompts = context["preprompt"]

    prev_user_prompts = context["user"]
    prev_assistant_responses = context["assistant"]

    # Send the pre-prompts as a system command to the gpt before everything else
    all_messages = [ {"role": "system", "content": preprompts} ]

    # Alternate between appending user prompts and assistant responses so that they are in order
    for i in range(len(prev_user_prompts)):
        all_messages.append({"role": "user", "content": prev_user_prompts[i]})

        # While there are assistant messages, append messages
        if i < len(context["assistant"]):
            all_messages.append(
                {"role": "assistant", "content": prev_assistant_responses[i]}
            )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
        n=1,
        max_tokens=168,
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(
        advance_generate_response(
            {
                "user": [
                    "Hello, I need help accessing my bank account",
                    "What was my last question?",
                ],
                "assistant": [
                    "You can access your account by going to the website and entering your credentials"
                ],
                "preprompt": "",
            },
        )
    )
