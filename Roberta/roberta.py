from transformers import pipeline  # type: ignore
import json
import pathlib

# Use the pipeline function to load the RoBERTa model
pipe = pipeline(
    "question-answering", model="deepset/roberta-base-squad2", device=-1
)  # Use GPU if available

# Example JSON object containing multiple users' bank information
context_json = {}
with open(str(pathlib.Path(__file__).parent.resolve()) + "/contexts.json",'r') as file:
        context_json = json.load(file)

# get_user_info is a helper function that takes in a user_name and pin and returns the user's account information
def get_user_info(user_name, pin):
    for user in context_json["contexts"]["bank"]["users"]:
        if user["name"].lower() == user_name.lower() and user["pin"] == pin:
            accounts_info = " ".join(
                [
                    f"{acc['account_type']} account with amount {acc['amount']}.\n"
                    for acc in user["accounts"]
                ]
            )
            return accounts_info
    return "User not found."

def get_accelerator_recommendation(company_name):
    for company in context_json["contexts"]["accelerator"]["companies"]:
        if company["name"].lower() == company_name.lower():
            implemented = company["implemented"]
            unimplemented = company["unimplemented"]
            accelerators = []
            for product in context_json["contexts"]["accelerator"]["products"]:
                if product["name"] in implemented:
                    accelerators.append(f"{product["name"]} can use this accelerator '{product["jumpstart"]}'")
                    #accelerators = f"{product["name"]} can use this accelerator {product["jumpstart"]}"
                elif product["name"] in unimplemented:
                    accelerators.append(f"{product["name"]} can use this accelerator '{product["tuneup"]}'")
            return " ".join(accelerators)

    return "Company not found."

def get_health(type):
    context = context_json["contexts"]["health"]["emergency_procedures"]
    for emergencyType in context:
        if emergencyType.lower() == type:
            for emergencyProcedure in context[type]:
                resources = []
                resources.append(context[type][emergencyProcedure]["description"]) 
                resources.append("you can contact them at")
                resources.append(context[type][emergencyProcedure]["phone"])
            return " ".join(resources)
        
    emergencyProcedure = context["general"]["Crisis Text Line"]
    resources = []
    resources.append(emergencyProcedure["description"]) 
    resources.append("you can contact them at")
    resources.append(emergencyProcedure["phone"])
    return " ".join(resources)


# roberta_response is an overloaded function that takes in a question and personality
# if the user_name and pin fields are filled and the personaility is a bank, it will operate as bank
# otherwise it will utitilize the personaility defined in personality field
def roberta_response(question, persona, user_name = None, pin = None):
    response = None

    if persona == "bank":
        context = get_user_info(user_name, pin)
        if context == "User not found.":
            return "User not found."
        response = pipe(question=question, context=context)

    elif persona == "accelerator":
        context = get_accelerator_recommendation(user_name)
        if context == "Company not found.":
            return "User not found."
        response = pipe(question=question, context=context)

    elif persona == "health":
        context = get_health(user_name)
        response = pipe(question=question, context=context)

    return response["answer"]


if __name__ == "__main__":
    user_name = "suicicde"
    product_name = "ServiceNow"
    type = "suicide"
    # pin = "9101"
    question = "What is the crisis hotline number"
    result = roberta_response(question, "health", type)
    print(result)
