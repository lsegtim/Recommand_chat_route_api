import spacy

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def train_bot(chatbot):
    trainer = ListTrainer(chatbot)
    trainer.train([
        "Hi",
        "Welcome, friend 🤗",
    ])
    trainer.train([
        "Are you a plant?",
        "No, I'm the pot below the plant!",
    ])

    return chatbot

def initialize_bot():

    try:
        nlp = spacy.load("en_core_web_md")
    except:
        spacy.cli.download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")

    chatbot = ChatBot("HistoMind")

    train = False

    if train:
        chatbot = train_bot(chatbot)

    exit_conditions = (":q", "quit", "exit")

    return chatbot, exit_conditions


def get_response(query, chatbot):
    return chatbot.get_response(query)


# while True:
#     query = input("> ")
#     if query in exit_conditions:
#         break
#     else:
#         print(f"🪴 {chatbot.get_response(query)}")
