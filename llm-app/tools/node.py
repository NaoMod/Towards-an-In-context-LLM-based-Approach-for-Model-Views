import json
from langchain_core.messages import FunctionMessage
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation

class ToolNode:
    def __init__(self, tools):
        self.tools = tools
        self.tool_executor = ToolExecutor(tools)

    def run_tool(self, state):
        """
        This runs tools in the graph

        It takes in an agent action and calls that tool and returns the result.

        Args:
            agent_action: The agent action to be executed.

        Returns:
            dict: A dictionary containing the response message.

        """
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
        response = self.tool_executor.invoke(action)
        # We use the response to create a FunctionMessage
        function_message = FunctionMessage(
            content=f"{tool_name} response: {str(response)}", name=action.tool
        )
        # We return a list, because this will get added to the existing list        
        return {"messages": [function_message]}

