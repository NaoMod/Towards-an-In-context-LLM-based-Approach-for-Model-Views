from typing import Sequence, TypedDict
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage

# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool

class AgentState(TypedDict):
    """State of an agent.

    Parameters
    ----------
    messages : Sequence[BaseMessage]
        List of messages received by the agent.
    sender : str
        Name of the sender agent.
    """
    messages: Sequence[BaseMessage]
    sender: str