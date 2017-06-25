# -*- coding: utf-8 -*-
from chatterbot import ChatBot

chatbot = ChatBot('Jarvis')

# Training with corpus data
# ChatterBot comes with a corpus data and utility module that makes it easy to quickly train the bot to communicate.
from chatterbot.trainers import ChatterBotCorpusTrainer

chatterbot = ChatBot("Training Example")
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train(
    "chatterbot.corpus.english"
)

response = chatterbot.get_response("Good morning!")
print(response)



