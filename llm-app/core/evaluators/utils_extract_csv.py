import os
from langsmith import Client

# Read the file and load the keys
script_dir = os.path.dirname(__file__)
rel_path = '../../token.txt'
abs_file_path = os.path.join(script_dir, rel_path)
token_file = open(abs_file_path, 'r')
# Ignore the first line
_ = token_file.readline()
langsmith_token_line = token_file.readline()

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = langsmith_token_line.split('=')[1].strip()

client = Client()

df = client.get_test_results(project_name="simplified_T:2_E:1-bd929658")
df.to_csv("results.csv", index=False)