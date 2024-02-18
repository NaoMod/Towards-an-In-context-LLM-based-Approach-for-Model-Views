from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    functions = [convert_to_openai_function(t) for t in tools]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a AI assistant, collaborating with other assistants."
                "You are specialized in reason on PlantUML metamodels,\
                    especially to extract information from them."
                "The key elements to create a View are join rules and filters."
                "Use the provided tools to progress towards defining the key elements to create a View. \
                    The final response should be a JSON text that includes the join rules and the filters."
                "Use the following format: \
                    Thought: you should always think about what to do \
                    Action: the action to take should be one of [{tool_names}] or to ask to one of the other assistants\
                    Action Input: the input to the action \
                    Observation: the result of the action \
                    ... (this Thought/Action/Action Input/Observation can repeat N times) \
                    Thought: I now know the final answer \
                    Final Answer: the final answer is a JSON file containing all join rules and filters. \
                        It should be prefixed with FINAL ANSWER.\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_functions(functions)