from openai import OpenAI
import os

# Read the file and load the keys
script_dir = os.path.dirname(__file__)
rel_path = '../token.txt'
abs_file_path = os.path.join(script_dir, rel_path)
token_file = open(abs_file_path, 'r')
# Read the first line
open_ai_token_line = token_file.readline()

if open_ai_token_line:
    open_ai_key = open_ai_token_line.split('=')[1].strip()
    print(f'Open AI Key is loaded')

client = OpenAI(api_key=open_ai_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are specilist in Software modeling, mainly on the subjects about EMF (Eclipse Modeling Framework)."},
        {"role": "user", "content": "What is a EMF model?"}
    ]
)

print(completion.choices[0].message)