class Edge:
    def __init__(self, state):
        self.state = state

    def router(self):
        """
        Either agent can decide to end

        Returns
        -------
        str
            The action to be taken by the router method. Possible values are:
            - "call_tool": if the previous agent is invoking a tool.
            - "end": if any agent has decided that the work is done.
            - "continue": if the work should continue.
        """
        messages = self.state["messages"]
        last_message = messages[-1]
        if "function_call" in last_message.additional_kwargs:
            # The previous agent is invoking a tool
            return "call_tool"
        if "FINAL ANSWER" in last_message.content:
            # Any agent decided the work is done
            return "end"
        return "continue"

