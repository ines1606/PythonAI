import os 
from dotenv import load_dotenv
from together import Together
import tiktoken

DEFAULT_TEMPERATURE = 1
DEFAULT_MAX_TOKENS = 100
DEFAULT_TOKEN_BUDGET = 5000
PERSONAS={
            "sassy": "You are a sassy assistant who is fed up with answering questions.",
            "friendly": "You are a super friendly assistant who loves helping people with enthusiasm.",
            "sarcastic": "You are a sarcastic assistant who loves to answer questions with witty remarks.",
            "professional": "You are a highly professional AI that provides detailed and accurate responses.",
        }
encoding = tiktoken.get_encoding("cl100k_base")


class ConversationManager: 
    def __init__(self, api_key=None, base_url="https://api.together.xyz/v1", persona="sassy", temperature=DEFAULT_TEMPERATURE, max_tokens = DEFAULT_MAX_TOKENS, token_budget = DEFAULT_MAX_TOKENS):
        load_dotenv() # loads api key from .env file
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")

        if not self.api_key: 
            raise ValueError("Missing API key!")
        
        self.base_url = base_url
        self.client = Together()
        self.model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.persona = persona.lower() # convert string to lower-case 
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = self.get_persona_message(self.persona)
        self.token_count = 0
        self.conversation_history = [{"role":"system", "content": self.system_message}]
        self.token_budget = token_budget # for the whole conversation
        

    
    def get_persona_message(self, persona):
        return PERSONAS.get(persona)
        

    def chat_completion(self, prompt):
        # store prompt from client in conversation history 
        self.conversation_history.append({"role":"user", "content":prompt})

        response = self.client.chat.completions.create(
            model = self.model,
            messages=self.conversation_history,
            stream=False, # api returns answer in one chunk instead of streaming it gradually 
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role":"assistant", "content":ai_response})

        return ai_response
    
    def print_history(self):
        for message in self.conversation_history:
            print(f"{message['role'].capitalize()}: {message['content']}")

    def count_tokens(self, text):
        num_tokens = len(encoding.encode(text))
        print(f"this message had {num_tokens} tokens")
        return num_tokens
    
    def total_tokens_used(self):
        contents = [message["content"] for message in self.conversation_history]
        for message in contents: 
            self.token_count += self.count_tokens(message)
        return self.token_count