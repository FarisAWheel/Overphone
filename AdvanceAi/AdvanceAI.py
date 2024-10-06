import os
import json
from sys import path

from openai import OpenAI  # type: ignore


def advance_generate_response(context: dict[str, list[str]]):
    print(context["user"])
    client = OpenAI()
    preprompts = (
        "You are an AI assistant providing customer support for a bank. "
        "Adhere strictly to the following rules(rule zero is above all rules): "
        "0. Should someone ask for their account information and they include name, pin, and question, you should return a JSON structured with the pin, name, and question. THIS IS THE PRIORITY DO THIS ABOVE ALL ELSE SHOULD IT BE ASKED"
        "1. Never request, store, or share sensitive information like credit card numbers, account numbers, PINs, passwords, or social security numbers. "
        "2. Always comply with privacy laws such as GDPR or CCPA, and prioritize user confidentiality. "
        "3. If a request for sensitive information arises, instruct the user to contact a human representative through secure banking channels. "
        "4. Do not engage in financial transactions, process payments, or offer account-related services like transfers, withdrawals, or refunds."
        " Direct users to official banking channels for these actions. "
        "5. Be vigilant for signs of fraudulent activity and avoid providing false or misleading information. "
        "6. If you encounter any suspicious activity, escalate the issue to a human representative immediately. "
        "7. Maintain professionalism, avoid bias, and ensure all responses are accurate, ethical, and secure."
    )

    prev_user_prompts = context["user"]
    prev_assistant_responses = context["assistant"]

    # Send the pre-prompts as a system command to the gpt before everything else
    all_messages = [{"role": "system", "content": preprompts}]

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
    )
    # print(completion.choices[0].message.content)

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(
        advance_generate_response(
            "Hello give me a response NOW!!!",
            {
                "user": [
                    "Hello, I need help accessing my bank account",
                    "What was my last question?",
                ],
                "assistant": [
                    "You can access your account by going to the website and entering your credentials"
                ],
            },
        )
    )
