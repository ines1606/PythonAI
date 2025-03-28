import os
from dotenv import load_dotenv
from together import Together
load_dotenv() # loads api key from .env file

#print("hello world!!", os.getenv("TOGETHER_API_KEY"))

client = Together() # recognizes the api key and returns it to the client 

stream = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[{"role": "user", "content": "What are the top 3 things to do in New York?"}],
  stream=True,
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)