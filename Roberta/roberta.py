from transformers import pipeline  # type: ignore

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
                    "creation_date": "2020-01-01",
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
                    "creation_date": "2021-02-20",
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
                    "creation_date": "2021-07-19",
                },
            ],
        },
    ]
}


def get_user_info(user_name, pin):
    for user in bank_info["users"]:
        if user["name"].lower() == user_name.lower() and user["pin"] == pin:
            accounts_info = " ".join(
                [
                    f"{acc['account_type']} account with amount {acc['amount']} created on {acc['creation_date']}.\n"
                    for acc in user["accounts"]
                ]
            )
            return accounts_info
    return "User not found."


def roberta_response(user_name, pin, question):
    context = get_user_info(user_name, pin)
    if context == "User not found.":
        return {"answer": context}

    response = pipe(question=question, context=context)

    return response


if __name__ == "__main__":
    user_name = "charlie"
    pin = "9100"
    question = "how much money does charlie have?"
    result = roberta_response(user_name, pin, question)
    print(result["answer"])
