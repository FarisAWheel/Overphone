from openai import OpenAI

def generate_response(preprompts: str, user_prompt: str):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": preprompts},
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return completion.choices[0].message

if __name__ == "__main__":
    print(generate_response("You are a helpful assistant", "Write a haiku about programming"))
