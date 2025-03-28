import os 
from dotenv import load_dotenv
from together import Together

DEFAULT_TEMPERATURE = 1
DEFAULT_MAX_TOKENS = 100
PERSONAS={
            "sassy": "You are a sassy assistant who is fed up with answering questions.",
            "friendly": "You are a super friendly assistant who loves helping people with enthusiasm.",
            "sarcastic": "You are a sarcastic assistant who loves to answer questions with witty remarks.",
            "professional": "You are a highly professional AI that provides detailed and accurate responses.",
        }

class ConversationManager: 
    def __init__(self, api_key=None, base_url="https://api.together.xyz/v1", persona="sassy", temperature=DEFAULT_TEMPERATURE, max_tokens = DEFAULT_MAX_TOKENS):
        load_dotenv() # loads api key from .env file
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        self.base_url = base_url
        self.client = Together()
        self.model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.persona = persona.lower() # convert string to lower-case 
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = self.get_persona_message(self.persona)
        self.conversation_history = [{"role":"system", "content": self.system_message}]

        if not self.api_key: 
            raise ValueError("Missing API key!")
        
        
    
    def get_persona_message(self, persona):
        return PERSONAS.get(persona)
        

    def chat_completion(self, prompt):
        # store prompt from client in conversation history 
        self.conversation_history.append({"role":"user", "content":prompt})
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[{"role":"system", "content": self.system_message},
                      {"role":"user", "content": prompt}],
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
