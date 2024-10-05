# analyzer.py is a module that analyzes the complexity of a given text
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure the necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('punkt_tab')

# Loads model for emotion classification
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

# The isComplex(text) function takes a text as input, returns 1 if text is comlex, 0 if simple
def isComplex(text):
    result = classifier(text)

    # Consider the text complex if the model detects anger, fear or sadness
    labelComplex = ["anger", "fear", "sadness"]
    emotionallyComplex = any(label['label'] in labelComplex for label in result)

    # Tokenize text into sentences
    sentences = sent_tokenize(text)

    # Calculate average sentence length
    avgSentLen = sum(len(word_tokenize(sentence)) for sentence in sentences)/len(sentences)

    # Consider the text complex if the average sentence length is greater than 20
    lengthComplex = avgSentLen > 20

    # Return true if text is complex either emotionally or length wise
    return emotionallyComplex or lengthComplex
