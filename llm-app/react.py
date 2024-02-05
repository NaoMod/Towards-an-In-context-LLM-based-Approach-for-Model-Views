from langchain import hub
from langchain.agents import Tool, create_react_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utilities import GoogleSerperAPIWrapper
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
from langchain_community.tools import DuckDuckGoSearchRun

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
        os.environ["LANGCHAIN_PROJECT"] = "APP"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = langsmith_key
    
    return open_ai_key

def main():
    st.title("Agent for Views")

    # Input from user are the plantUML models as txt files
    uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'])
    uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'])

    # Input from user
    input_text = st.text_area("Enter your text:")
    
    if st.button("Run Agent"):

        def toggle_case(word):
            toggled_word = ""
            for char in word:
                if char.islower():
                    toggled_word += char.upper()
                elif char.isupper():
                    toggled_word += char.lower()
                else:
                    toggled_word += char
            return toggled_word

        def sort_string(string):
            return ''.join(sorted(string))
        
        search = DuckDuckGoSearchRun()

        tools = [
                Tool(
                    name = "DuckDuckGo",
                    func=search,
                    description="useful for when you need to search for information",
                ),
                Tool(
                    name = "Toogle_Case",
                    func = lambda word: toggle_case(word),
                    description = "use when you want covert the letter to uppercase or lowercase",
                ),
                Tool(
                    name = "Sort String",
                    func = lambda string: sort_string(string),
                    description = "use when you want sort a string alphabetically",
                ),

        ]
        
        prompt = hub.pull("hwchase17/react")

        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=read_tokens())

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

