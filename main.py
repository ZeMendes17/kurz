from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
print(classifier("I love this!"))

