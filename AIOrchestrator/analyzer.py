# analyzer.py is a module that analyzes the complexity of a given text
from transformers import pipeline


# Loads model for emotion classification
try:
    classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
except: 
    print("Error loading model")

# The isComplex(text) function takes a text as input, returns 1 if text is comlex, 0 if simple
def isComplex(text):
    result = classifier(text)

    # Consider the text complex if the model detects anger, fear or sadness
    labelComplex = ["anger", "fear", "sadness"]
    emotionallyComplex = any(label['label'] in labelComplex and label['score'] > 0.67 for label in result)

    # Tokenize text into sentences
    words = text.split(" ")
    print(f'result: {result}')

    # Consider the text complex if there are over 20 sentences
    lengthComplex = len(words) > 100

    # Return true if text is complex either emotionally or length wise
    return emotionallyComplex or lengthComplex

