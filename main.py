import os
from dotenv import load_dotenv
from together import Together
import ConversationManager as c
load_dotenv() # loads api key from .env file

#print("hello world!!", os.getenv("TOGETHER_API_KEY"))

c_manager = c.ConversationManager(persona = "sassy")

while True: 
    user_input = input("Du: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    response = c_manager.chat_completion(user_input)

    print("Bot: ", end="", flush=True)
    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")

