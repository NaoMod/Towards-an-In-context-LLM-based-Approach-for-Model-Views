import os

# Read the file and load the keys
token_file = open('../token.txt', 'r')
# Read the first line
open_ai_token_line = token_file.readline()

if open_ai_token_line:
    open_ai_key = open_ai_token_line.split('=')[1].strip()
    print(f'Open AI Key  is loaded')

# Read the second line
langsmith_token_line = token_file.readline()

if langsmith_token_line:
    langsmith_key = langsmith_token_line.split('=')[1].strip()
    print(f'Langsmith Key is loaded')


if langsmith_key is not None:
    # Configure LangSmith
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "MULTI-AGENT"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key