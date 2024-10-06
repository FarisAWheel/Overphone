from transformers import pipeline  # type: ignore
import json
import os

# Use the pipeline function to load the RoBERTa model
pipe = pipeline(
    "question-answering", model="deepset/roberta-base-squad2", device=-1
)  # Use GPU if available

# Example JSON object containing multiple users' bank information
bank_info = {
    "users": [
        {
            "name": "Alice",
            "pin": "1234",
            "accounts": [
                {
                    "account_type": "savings",
                    "amount": 5000,
                },
            ],
        },
        {
            "name": "Bob",
            "pin": "5678",
            "accounts": [
                {
                    "account_type": "checking",
                    "amount": 3000,
                },
            ],
        },
        {
            "name": "Charlie",
            "pin": "9101",
            "accounts": [
                {
                    "account_type": "business",
                    "amount": 10000,
                },
            ],
        },
    ]
}

# Load contexts loads the json file containing all contexts
def load_contexts():
    with open(os.path.join(os.path.dirname(__file__), "contexts.json"), "r") as file:
        return json.load(file)["contexts"]
    
contexts = load_contexts()

def get_user_info(user_name, pin):
    for user in bank_info["users"]:
        if user["name"].lower() == user_name.lower() and user["pin"] == pin:
            accounts_info = " ".join(
                [
                    f"{acc['account_type']} account with amount {acc['amount']}.\n"
                    for acc in user["accounts"]
                ]
            )
            return accounts_info
    return "User not found."

# The roberta_response function takes in a question, it's overloaded with user_name and pin for the bank persona
# The overloaded version utilizes the pre-existing get_user_info() function to retrieve the user's information accurately
def roberta_response(question, persona, user_name=None, pin=None):
    if(persona == "bank"): 
        context = get_user_info(user_name, pin)
        if context == "User not found.":
            return "User not found."

        response = pipe(question=question, context=context)

    return response["answer"]


if __name__ == "__main__":
    user_name = "charlie"
    pin = "9101"
    question = "how much money does charlie have?"
    result = roberta_response(question, "bank", user_name, pin)
    print(result)
