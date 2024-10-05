# Import the required modules
from transformers import pipeline  # type: ignore

# Use the pipeline function to load the GPT-2 model
pipe = pipeline("text-generation", model="gpt2", device=0)  # Use GPU if available


# Define a function to generate a haiku
def generate_haiku(prompt):
    result = pipe(
        prompt,
        num_return_sequences=1,
        truncation=True,
        clean_up_tokenization_spaces=True,
        pad_token_id=pipe.model.config.eos_token_id,
    )
    return result[0]["generated_text"]


if __name__ == "__main__":
    # Use the function to generate a haiku with a given prompt
    prompt = "Write a haiku about the ocean. Make sure to end on punctuation."
    haiku = generate_haiku(prompt)
    print(haiku)
