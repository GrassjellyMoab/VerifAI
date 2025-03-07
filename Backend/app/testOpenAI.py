from utils.config import OPENAI_API_KEY

from openai import OpenAI

client = OpenAI(
  api_key=OPENAI_API_KEY
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
