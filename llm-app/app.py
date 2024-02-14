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

is_configured = False

# Streamlit configurations
st.set_page_config(page_title="🔗 Views helper")
st.title('🔗 Views helper')

# Load PlantUML file
def load_txt(input_file):
  with st.expander('See Model'):
    st.write(input_file)
  return input_file


def generate_response(uploaded_file_1, uplodaded_file_2, query_text):
   
    if uploaded_file_1 is not None and uplodaded_file_2 is not None:
        
        response = agent.invoke(query_text)
        return response
    

# question_list = [
#   'How many rows are there?',
#   'What is the range of values for MolWt with logS greater than 0?',
#   'How many rows have MolLogP value greater than 0.',
#   'Other']
# query_text = st.selectbox('Select an example query:', question_list, disabled=not (uploaded_file_1 and uploaded_file_2))

if 'history' not in st.session_state:
    st.session_state['history'] = []

# Initialize messages
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Explain what you want for this View " + " 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey ! 👋"]

# Create containers for chat history and user input
response_container = st.container()
container = st.container()

with container:
    # Input widgets
    uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'])
    uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'])
    # # Query text
    # query_text = st.text_input('Start the proccess:', placeholder = 'View task details', disabled=not (uploaded_file_1 and uploaded_file_2))
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Query:", placeholder="View task details", key='input')
        submit_button = st.form_submit_button(label='Send')
    if uploaded_file_1 and  uploaded_file_2 and user_input :
        st.session_state['past'].append(user_input )
        response = generate_response(uploaded_file_1, uploaded_file_2, user_input)
        st.session_state['generated'].append(response)
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


# Form input and query
# result = []
# with st.form('myform', clear_on_submit=True):
#     submitted = st.form_submit_button('Submit', disabled=not(uploaded_file_1 and  uploaded_file_2 and query_text))
#     if submitted:
#         with st.spinner('Thinking...'):
#             response = generate_response(uploaded_file_1, uploaded_file_2, query_text)
#             result.append(response)

# if len(result):
#     st.info(response)