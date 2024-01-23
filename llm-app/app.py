##LLM app

from langchain_community.vectorstores import Chroma
import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain.agents import AgentType, initialize_agent, Tool

import streamlit as st
from langchain_community.llms import OpenAI

#Load OpenAI API key and LangSmith API key
script_dir = os.path.dirname(__file__)
tokenFile = open(os.path.join(script_dir, '../open_ai_token.txt'), 'r')
token = tokenFile.readline()
key = token.split('=')[1].strip()
langsmithtoken = tokenFile.readline()
langsmithkey = langsmithtoken.split('=')[1].strip()

print("The API keys are loaded")

#configure LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "APP"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = langsmithkey

st.set_page_config(page_title="🔗 Views helper")
st.title('🔗 Views helper')

# def generate_response(topic):
#   llm = OpenAI(temperature=0.7, openai_api_key=key)
#   # Prompt
#   template = 'As an experienced data scientist and technical writer, generate an outline for a blog about {topic}.'
#   prompt = PromptTemplate(input_variables=['topic'], template=template)
#   prompt_query = prompt.format(topic=topic)
#   # Run LLM model and print out response
#   response = llm(prompt_query)
#   return st.info(response)

# Load PlantUML file
def load_txt(input_file):
  with st.expander('See Model'):
    st.write(input_file)
  return input_file

tools = []

def generate_response(uploaded_file_1, uplodaded_file_2, query_text):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=key)
    if uploaded_file_1 is not None and uplodaded_file_2 is not None:
        documents = [{"name": uploaded_file_1.name[:-4], "content": uploaded_file_1.read().decode()}, {"name": uplodaded_file_2.name[:-4], "content": uplodaded_file_2.read().decode()}]
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        texts = text_splitter.create_documents(list(d['content'] for d in documents))
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain inside a tool
        tools.append(
            Tool(
                name=documents[0]["name"],
                description=f"useful when you want to answer questions about {documents[0]['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever),
            )
        )
        tools.append(
            Tool(
                name=documents[1]["name"],
                description=f"useful when you want to answer questions about {documents[1]['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever),
            )
        )

        agent = initialize_agent(
            agent=AgentType.OPENAI_FUNCTIONS,
            tools=tools,
            llm=llm,
            verbose=True,
        )
        response = agent.run(query_text)
        return st.success(response)
    
# Input widgets
uploaded_file_1 = st.file_uploader('Upload 1st PlantUML model', type=['txt'])
uploaded_file_2 = st.file_uploader('Upload 2nd PlantUML model', type=['txt'])
question_list = [
  'How many rows are there?',
  'What is the range of values for MolWt with logS greater than 0?',
  'How many rows have MolLogP value greater than 0.',
  'Other']
query_text = st.selectbox('Select an example query:', question_list, disabled=not uploaded_file)

# Query text
# query_text = st.text_input('Start the proccess:', placeholder = 'View task details', disabled=not (uploaded_file_1 and uploaded_file_2))


# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file_1 and  uploaded_file_2 and query_text))
    if submitted:
        with st.spinner('Thinking...'):
            response = generate_response(uploaded_file_1, uploaded_file_2, query_text)
            result.append(response)

if len(result):
    st.info(response)