from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate  
from langchain_openai import ChatOpenAI  
from langchain_core.runnables import RunnablePassthrough

from utils.config import Config
import json

config = Config()
config.load_keys()

# Function to print JSON keys
def print_json_keys(json_output):
    r = json.dumps(json_output)
    data = json.loads(r)
    print("Keys:", data.keys())
    return data

llm = ChatOpenAI(temperature=0, api_key=config.get_open_ai_key())

joke_for_topic_prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}.")
output_parser1 = StrOutputParser()

analyze_joke_prompt = ChatPromptTemplate.from_template("What is the joke below about?\n{joke}. Answer it with a JSON object.")
output_parser2 = JsonOutputParser()

# Chain
chain = (
    {"topic": RunnablePassthrough()}
    | joke_for_topic_prompt
    | llm
    | {"joke": output_parser1}
    | analyze_joke_prompt
    | llm
    | output_parser2
    | print_json_keys
)

# Invoke the chain
result = chain.invoke({"topic": "ice cream"})

print(result)