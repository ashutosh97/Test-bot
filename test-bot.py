# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import logging


# Create a new instance of a ChatBot
bot = ChatBot("Jarvis", # Name of bot - Jarvis
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation", # For mathematical calculation
        "chatterbot.logic.TimeLogicAdapter", # For current time
        "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="./database.json"
)

print("Hello! I am Jarvis ")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
