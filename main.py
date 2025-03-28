import os
from dotenv import load_dotenv
from together import Together
import ConversationManager as c
load_dotenv() # loads api key from .env file

#print("hello world!!", os.getenv("TOGETHER_API_KEY"))

def get_persona():
    persona_input = input("Choose persona:\n [sassy, friendly, sarcastic, professional] \n-> ")

    while persona_input not in c.PERSONAS: 
        print("Not a valid persona, try again!")
        persona_input = input("-> ")
    return persona_input

def get_temperature(): 
    while True:
        try:
            temperature = float(input("Choose degree of precision between 0 (very precise) and 1 (least precise) \n-> "))
            if 0 <= temperature <= 1:
                return temperature
            else:
                print("Invalid precision! Please enter a value between 0 and 1.")
        except ValueError:
            print("Please enter a valid number.")

def get_max_tokens():
    while True:
        try:
            max_tokens = int(input("Choose amount of tokens used by answer between 50 and 500\n-> "))
            if 50 <= max_tokens <= 500:
                return max_tokens
            else:
                print("Invalid number of tokens! Please enter a value between 50 and 500.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("start")
    c_manager = c.ConversationManager(persona = get_persona(), temperature=get_temperature(), max_tokens=get_max_tokens())

    while True: 
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        if user_input.lower() == "history":
            print(c_manager.print_history())
        else:
            response = c_manager.chat_completion(user_input)

            print("Bot: ", end="", flush=True)
            for chunk in response:
                print(chunk, end="", flush=True)
        print("\n")

        
        #print(f"history: {c_manager.print_history()}") 
        

if __name__ == "__main__":
    main()

