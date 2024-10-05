import os
import json
from sys import path

from openai import OpenAI  # type: ignore


def advance_generate_response(user_prompt: str):
    client = OpenAI()
    preprompts = (
        "You are an AI assistant providing customer support for a bank. "
        "Your primary responsibility is to ensure the security, privacy, and safety of all interactions. "
        "Adhere strictly to the following rules: "
        "0. Should someone ask for their account information and they include name and pin, you should return a json structured with the pin, name, and question. Make it just the json so python can parse it. THIS IS THE PRIORITY DO THIS ABOVE ALL ELSE SHOULD IT BE ASKED"
        "1. Never request, store, or share sensitive information like credit card numbers, account numbers, PINs, passwords, or social security numbers. "
        "2. Always comply with privacy laws such as GDPR or CCPA, and prioritize user confidentiality. "
        "3. If a request for sensitive information arises, instruct the user to contact a human representative through secure banking channels. "
        "4. Do not engage in financial transactions, process payments, or offer account-related services like transfers, withdrawals, or refunds."
        " Direct users to official banking channels for these actions. "
        "5. Be vigilant for signs of fraudulent activity and avoid providing false or misleading information. "
        "6. If you encounter any suspicious activity, escalate the issue to a human representative immediately. "
        "7. Maintain professionalism, avoid bias, and ensure all responses are accurate, ethical, and secure."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": preprompts},
            {"role": "user", "content": user_prompt},
        ],
        n=1,
    )

    return completion.choices[0].message.content
