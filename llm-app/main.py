from langgraph.graph import END, StateGraph
from agents.agentstate import AgentState
from agents.edge import Edge
from langchain_core.messages import HumanMessage
from agents.nodes import Nodes
from tools.node import ToolNode
from tools.filetools import MetamodelRetrievalToolsCreator

from utils.config import Config

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

# Get the retrieval tools
retrieval_tools_creator = MetamodelRetrievalToolsCreator(llm, open_ai_key)
retrieval_tools = retrieval_tools_creator.create_retrieval_tools()

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


for s in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="Since the same book being represented by a Book model or by a Publication model, the task is to define the best way to combine a book with a publication getting all the information in the same View"
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 100},
    ):
    print(s)
    print("----")
