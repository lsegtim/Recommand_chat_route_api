import random

import spacy
import yaml
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load spaCy model and dataset
nlp = spacy.load("en_core_web_md")

with open("conversations.yml", "r") as file:
    dataset = yaml.safe_load(file)

# Function to extract recognized entities
def extract_entities(user_input):
    doc = nlp(user_input)
    entities = [ent.text for ent in doc.ents]
    return entities

# Function for similarity search
def find_similar_response(user_input):
    user_entities = extract_entities(user_input)
    best_match = None
    best_score = 0

    for item in dataset:
        question = item[0]
        score = cosine_similarity(vectorizer.transform([user_input]), vectorizer.transform([question]))[0][0]

        if score > best_score:
            best_score = score
            best_match = random.choice(item[1:])  # Randomly select an answer

    if best_match:
        return best_match
    else:
        return "I'm sorry, I don't have information about that."

# Vectorize the dataset for similarity search
corpus = [item[0] for item in dataset]
print(corpus)
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)

# Main chatbot loop
def find_entity_based_response(entity):
    for item in dataset:
        if entity in item[0]:
            return random.choice(item[1:])  # Randomly select an answer

    return None


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    entities = extract_entities(user_input)
    print("Entities:", entities)

    if entities:
        # Prioritize entity-based responses
        for entity in entities:
            response = find_entity_based_response(entity)
            if response:
                print("Chatbot:", response)
                break  # Stop after the first relevant response
        else:
            # No entity-based responses found, use similarity search
            response = find_similar_response(user_input)
            print("Chatbot:", response)
    else:
        # No recognized entities, use similarity search
        response = find_similar_response(user_input)
        print("Chatbot:", response)
