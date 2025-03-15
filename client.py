from dotenv import load_dotenv
import os

load_dotenv()

openaiapikey = os.getenv('OPENAIAPIKEY')


from openai import OpenAI

client = OpenAI(
  api_key=openaiapikey
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "system", "content": "You are a virtual assistant named siri skilled in general tasks like alexa and google cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)
