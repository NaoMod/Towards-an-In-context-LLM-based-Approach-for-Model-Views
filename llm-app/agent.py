from langchain import hub
from langchain.agents import Tool, create_react_agent
from langchain_openai import ChatOpenAI
import os
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator
from typing import TypedDict, Annotated
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.prebuilt import ToolInvocation
from langgraph.graph import END, StateGraph
from langchain_core.agents import AgentActionMessageLog
import streamlit as st
import json

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
)
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation
from langchain_core.tools import tool
from typing import Annotated
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import Chroma
import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain.agents import AgentType, initialize_agent, Tool
import operator
from typing import Annotated, List, Sequence, Tuple, TypedDict, Union
import functools
from langchain.agents import create_openai_functions_agent
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, FunctionMessage):
        pass
    else:
        result = HumanMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }

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

def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    functions = [format_tool_to_openai_function(t) for t in tools]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards defining the key elements to create a View. \
                    The final response should be a JSON text that includes filters, join rules and the potential comparisons."
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop."
                " You have access to the following tools: {tool_names}.\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_functions(functions)

def get_tools_for_metamodels(llm, open_ai_key, tools, uploaded_file_1, uploaded_file_2):
    tools = []    
    if uploaded_file_1 is not None and uploaded_file_2 is not None:
        documents = [{"name": uploaded_file_1.name[:-4], "content": uploaded_file_1.read().decode()}, {"name": uploaded_file_2.name[:-4], "content": uplodaded_file_2.read().decode()}]
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
                description=f"useful when you need to analyze the document {documents[0]['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever),
            )
        )
        tools.append(
            Tool(
                name=documents[1]["name"],
                description=f"useful when you need to analyze the document {documents[1]['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever),
            )
        )
    return tools

def tool_node(state, tool_executor):
    """This runs tools in the graph

    It takes in an agent action and calls that tool and returns the result."""
    messages = state["messages"]
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    tool_input = json.loads(
        last_message.additional_kwargs["function_call"]["arguments"]
    )
    # We can pass single-arg inputs by value
    if len(tool_input) == 1 and "__arg1" in tool_input:
        tool_input = next(iter(tool_input.values()))
    tool_name = last_message.additional_kwargs["function_call"]["name"]
    action = ToolInvocation(
        tool=tool_name,
        tool_input=tool_input,
    )
    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(
        content=f"{tool_name} response: {str(response)}", name=action.tool
    )
    # We return a list, because this will get added to the existing list
    return {"messages": [function_message]}

def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        # The previus agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "end"
    return "continue"

def main():
    st.set_page_config(
        page_title="Agent for Views", page_icon="🔗", layout="wide", initial_sidebar_state="collapsed"
    )

    # Input widgets
    uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'])
    uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'])

    # TODO: Add a text area for the user to input text
    # TODO: Create tools for specific parts of the View definition

    open_ai_key = read_tokens()

    llm = ChatOpenAI(model="gpt-3.5-turbo-0613", openai_api_key=open_ai_key)

    join_tools = get_tools_for_metamodels(llm, open_ai_key, tools, uploaded_file_1, uploaded_file_2)

    # CreateJoin agent  node
    create_join_agent = create_agent(
        llm, 
        [join_tools],
        system_message="You should provide accurate data for the chart generator to use.",
    )
    create_join_node = functools.partial(agent_node, agent=create_join_agent, name="CreateJoin")

    # # Chart Generator
    # chart_agent = create_agent(
    #     llm,
    #     [python_repl],
    #     system_message="Any charts you display will be visible by the user.",
    # )
    # chart_node = functools.partial(agent_node, agent=chart_agent, name="Chart Generator")

    tool_executor = ToolExecutor(join_tools)

    workflow = StateGraph(AgentState)

    workflow.add_node("CreateJoin", create_join_node)
    # workflow.add_node("Chart Generator", chart_node)
    workflow.add_node("call_tool", tool_node)

    workflow.add_conditional_edges(
        "CreateJoin",
        router,
        {"continue": "Chart Generator", "call_tool": "call_tool", "end": END},
    )
    # workflow.add_conditional_edges(
    #     "Chart Generator",
    #     router,
    #     {"continue": "CreateJoin", "call_tool": "call_tool", "end": END},
    # )

    workflow.add_conditional_edges(
        "call_tool",
        # Each agent node updates the 'sender' field
        # the tool calling node does not, meaning
        # this edge will route back to the original agent
        # who invoked the tool
        lambda x: x["sender"],
        {
            "CreateJoin": "CreateJoin",
            # "Chart Generator": "Chart Generator",
        },
    )
    workflow.set_entry_point("CreateJoin")
    graph = workflow.compile()


