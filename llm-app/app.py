##LLM app

import streamlit as st
from streamlit_chat import message

from langgraph.graph import END, StateGraph
from agents.agentstate import AgentState
from agents.edge import Edge
from agents.nodes import Nodes
from tools.node import ToolNode
from tools.filetools import MetamodelRetrievalToolsCreator
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_community.callbacks import StreamlitCallbackHandler

from utils.st_utility import configure, with_clear_container

# Set up Streamlit configurations
st.set_page_config(page_title="Views helper", page_icon="🔗")
st.title('🔗 Views helper')
# st.header(":green[_LLM_]", divider="red")
st.caption(":violet[_EMF Views assistant_]")
st.sidebar.subheader("__Files Panel__")

# Input widgets
uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'], help="PlantUML")
uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'], help="PlantUML")

if not uploaded_file_1 or not uploaded_file_2:
    st.info("Please upload the models to continue.")
    st.stop()

llm, open_ai_key = configure()

documents = [
    {"name": uploaded_file_1.name[:-4], "content": uploaded_file_1.read().decode()}, 
    {"name": uploaded_file_2.name[:-4], "content": uploaded_file_2.read().decode()}
]

 # Get the retrieval tools
retrieval_tools_creator = MetamodelRetrievalToolsCreator(llm, open_ai_key)
retrieval_tools = retrieval_tools_creator.create_retrieval_tools(documents=documents)

# Get the agent and tool nodes
nodes = Nodes(llm, retrieval_tools)
get_join_rules_node = nodes.join_rules_node()
filter_generator_node = nodes.filter_generator_node()
tool_node = ToolNode(retrieval_tools)

workflow = StateGraph(AgentState)

workflow.add_node("GetJoinRules", get_join_rules_node)
workflow.add_node("FilterGenerator", filter_generator_node)
workflow.add_node("call_tool", tool_node.run_tool)

workflow.add_conditional_edges(
    "GetJoinRules",
    Edge.router,
    {"continue": "FilterGenerator", "call_tool": "call_tool", "end": END},
)
workflow.add_conditional_edges(
    "FilterGenerator",
    Edge.router,
    {"continue": "GetJoinRules", "call_tool": "call_tool", "end": END},
)

workflow.add_conditional_edges(
    "call_tool",
    # Each agent node updates the 'sender' field
    # the tool calling node does not, meaning
    # this edge will route back to the original agent
    # who invoked the tool
    lambda x: x["sender"],
    {
        "GetJoinRules": "GetJoinRules",
        "FilterGenerator": "FilterGenerator",
    },
)
workflow.set_entry_point("GetJoinRules")
graph = workflow.compile()

with st.form(key="form"):
    user_input = st.text_input("Define the task for the View")
    submit_clicked = st.form_submit_button("Generate")

output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)

    answer_container = output_container.chat_message("assistant", avatar="🦜")
    # st_callback = StreamlitCallbackHandler(answer_container)
    cfg = RunnableConfig()
    # cfg["callbacks"] = [st_callback]
    cfg["recursion_limit"] = 100
    cfg["tags"] = ["Experiment_1"]

    answer = graph.invoke({
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ],
        }, cfg)

    answer_container.write(answer)