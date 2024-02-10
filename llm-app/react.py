from langchain import hub
from langchain.agents import Tool, create_react_agent
from langchain_openai import ChatOpenAI
import os
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.prebuilt import ToolInvocation
from langgraph.graph import END, StateGraph
from langchain_core.agents import AgentActionMessageLog
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

st.set_page_config(page_title="Agent for Views", layout="wide")

def read_tokens():
    # Read the file and load the keys
    script_dir = os.path.dirname(__file__)
    token_file_path = os.path.join(script_dir, 'token.txt')

    langsmith_key = None
    open_ai_key = None

    with open(token_file_path, 'r') as token_file:
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
    
    return open_ai_key

def main():
    st.title("Agent for Views")

    # Input from user are the plantUML models as txt files
    uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'])
    uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'])

    # Input from user
    input_text = st.text_area("Enter your task:")
    
    if st.button("Run Agent"):
        open_ai_key = read_tokens()
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=open_ai_key)

        tools = []

        documents = [
            {"name": uploaded_file_1.name[:-4], "content": uploaded_file_1.read().decode()}, 
            {"name": uploaded_file_2.name[:-4], "content": uploaded_file_2.read().decode()}
        ]
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        texts = text_splitter.create_documents(list(d['content'] for d in documents))
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=open_ai_key)
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
    
        # prompt = hub.pull("hwchase17/react")
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a AI assistant, specialized in reason on PlantUML metamodels serialized as txt files,\
                        especially combining and merging them into an object called View."
                    "The key elements to create a View are filters, join rules and potential comparisons between its elements."
                    " Use the provided tools to progress towards defining the key elements to create a View. \
                        The final response should be a JSON text that includes filters, join rules and the potential comparisons."
                    " You have access to the following tools: {tool_names}."
                    "Use the following format: \
                        Metamodels: the input metamodels for which you must provide an answer. They are paths to two metamodels in the filesystem separated by a comma \
                        Thought: you should always think about what to do \
                        Action: the action to take should be one of [{tool_names}] \
                        Action Input: the input to the action \
                        Observation: the result of the action \
                        ... (this Thought/Action/Action Input/Observation can repeat N times) \
                        Thought: I now know the final answer \
                        Final Answer: the final answer to the original input metamodels \
                        Metamodels: {input} \
                        {agent_scratchpad}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        # prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))

        agent_runnable = create_react_agent(llm, tools, prompt)

        class AgentState(TypedDict):
            input: str
            chat_history: list[BaseMessage]
            agent_outcome: Union[AgentAction, AgentFinish, None]
            return_direct: bool
            intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

        tool_executor = ToolExecutor(tools)

        def run_agent(state):
            
            inputs = state.copy()
            if len(inputs['intermediate_steps']) > 5:
                inputs['intermediate_steps'] = inputs['intermediate_steps'][-5:]

            agent_outcome = agent_runnable.invoke(state)
            return {"agent_outcome": agent_outcome}
        
        def execute_tools(state):

            messages = [state['agent_outcome'] ]
            last_message = messages[-1]

            ######### human in the loop ###########   
            # human input y/n 
            # Get the most recent agent_outcome - this is the key added in the `agent` above
            # state_action = state['agent_outcome']
            # human_key = input(f"[y/n] continue with: {state_action}?")
            # if human_key == "n":
            #     raise ValueError
            
            tool_name = last_message.tool
            arguments = last_message
            if tool_name == "Search" or tool_name == "Sort" or tool_name == "Toggle_Case":
                
                if "return_direct" in arguments:
                    del arguments["return_direct"]
            action = ToolInvocation(
                tool=tool_name,
                tool_input= last_message.tool_input,
            )
            response = tool_executor.invoke(action)
            return {"intermediate_steps": [(state['agent_outcome'],response)]}
        
        def should_continue(state):

            messages = [state['agent_outcome'] ] 
            last_message = messages[-1]
            if "Action" not in last_message.log:
                return "end"
            else:
                arguments = state["return_direct"]
                if arguments is True:
                    return "final"
                else:
                    return "continue"
                
        def first_agent(inputs):
            action = AgentActionMessageLog(
                tool="Search",
                tool_input=inputs["input"],
                log="",
                message_log=[]
            )
            return {"agent_outcome": action}
        
        workflow = StateGraph(AgentState)

        workflow.add_node("agent", run_agent)
        workflow.add_node("action", execute_tools)
        workflow.add_node("final", execute_tools)
        # uncomment if you want to always calls a certain tool first
        # workflow.add_node("first_agent", first_agent)


        workflow.set_entry_point("agent")
        # uncomment if you want to always calls a certain tool first
        # workflow.set_entry_point("first_agent")

        workflow.add_conditional_edges(

            "agent",
            should_continue,

            {
                "continue": "action",
                "final": "final",
                "end": END
            }
        )


        workflow.add_edge('action', 'agent')
        workflow.add_edge('final', END)
        # uncomment if you want to always calls a certain tool first
        # workflow.add_edge('first_agent', 'action')
        app = workflow.compile()

        inputs = {"input": input_text, "chat_history": [], "return_direct": False}
        results = []
        for s in app.stream(inputs):
            result = list(s.values())[0]
            results.append(result)
            st.write(result)  # Display each step's output


if __name__ == "__main__":
    main()

