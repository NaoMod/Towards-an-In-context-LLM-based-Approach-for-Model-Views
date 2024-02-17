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

from utils.st_utility import configure

# A hack to "clear" the previous result when submitting a new prompt. This avoids
# the "previous run's text is grayed-out but visible during rerun" Streamlit behavior.
class DirtyState:
    NOT_DIRTY = "NOT_DIRTY"
    DIRTY = "DIRTY"
    UNHANDLED_SUBMIT = "UNHANDLED_SUBMIT"


def get_dirty_state() -> str:
    return st.session_state.get("dirty_state", DirtyState.NOT_DIRTY)


def set_dirty_state(state: str) -> None:
    st.session_state["dirty_state"] = state


def with_clear_container(submit_clicked: bool) -> bool:
    if get_dirty_state() == DirtyState.DIRTY:
        if submit_clicked:
            set_dirty_state(DirtyState.UNHANDLED_SUBMIT)
            st.experimental_rerun()
        else:
            set_dirty_state(DirtyState.NOT_DIRTY)

    if submit_clicked or get_dirty_state() == DirtyState.UNHANDLED_SUBMIT:
        set_dirty_state(DirtyState.DIRTY)
        return True

    return False


# Set up Streamlit configurations
st.set_page_config(page_title="Views helper", page_icon="🔗")
st.title('🔗 Views helper')
st.header(":green[_Welcome_]", divider="red")
st.caption(":violet[_EMF Views assistant_]")
st.sidebar.subheader("__Files Panel__")

# Input widgets
uploaded_file_1 = st.sidebar.file_uploader('1st PlantUML model', type=['txt'], help="PlantUML")
uploaded_file_2 = st.sidebar.file_uploader('2nd PlantUML model', type=['txt'], help="PlantUML")

if not uploaded_file_1 or not uploaded_file_2:
    st.info("Please upload the models to continue.")
    st.stop()

llm, open_ai_key = configure()

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

# Display user input field and enter button
if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    # Display assistant response
    with st.chat_message("assistant"):
        # Check for the presence of the "messages" key in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        response = graph.invoke(
            {
            "messages": [
                HumanMessage(
                    content=user_query
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 100}
        )
        st.toast("Success!", icon="✅")

    # with st.form(key="form"):
    #     user_input = st.text_input("Define the task")
    #     submit_clicked = st.form_submit_button("Run agent")

    # output_container = st.empty()
    # if with_clear_container(submit_clicked):
    
    #     output_container = output_container.container()
    #     output_container.chat_message("user").write(user_input)

    #     answer_container = output_container.chat_message("assistant", avatar="🦜")
    #     st_callback = StreamlitCallbackHandler(answer_container)
    #     cfg = RunnableConfig()
    #     cfg["callbacks"] = [st_callback]

    #     answer = graph.invoke(
    #         {
    #             "messages": [
    #                 HumanMessage(
    #                     content=user_input
    #                 )
    #             ]
    #         },
    #         {"recursion_limit": 100})

# Load PlantUML file
def load_txt(input_file):
  with st.expander('See Model'):
    st.write(input_file)
  return input_file


# def generate_response(uploaded_file_1, uplodaded_file_2, query_text):
   
#     if uploaded_file_1 is not None and uplodaded_file_2 is not None:
        
#         response = agent.invoke(query_text)
#         return response
    

# question_list = [
#   'How many rows are there?',
#   'What is the range of values for MolWt with logS greater than 0?',
#   'How many rows have MolLogP value greater than 0.',
#   'Other']
# query_text = st.selectbox('Select an example query:', question_list, disabled=not (uploaded_file_1 and uploaded_file_2))

# if 'history' not in st.session_state:
#     st.session_state['history'] = []

# # Initialize messages
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = ["Hello ! Explain the task you want for this View " + " 🤗"]

# if 'past' not in st.session_state:
#     st.session_state['past'] = ["Hey ! 👋"]

# Create containers for chat history and user input
# response_container = st.container()
# container = st.container()

# with container:
    
#     # # Query text
#     # query_text = st.text_input('Start the proccess:', placeholder = 'View task details', disabled=not (uploaded_file_1 and uploaded_file_2))
#     with st.form(key='my_form', clear_on_submit=True):
#         user_input = st.text_input("Query:", placeholder="View task details", key='input')
#         submit_button = st.form_submit_button(label='Run Agent')
#     if uploaded_file_1 and  uploaded_file_2 and user_input :
#         st.session_state['past'].append(user_input )
#         response = generate_response(uploaded_file_1, uploaded_file_2, user_input)
#         st.session_state['generated'].append(response)
#     if st.session_state['generated']:
#         with response_container:
#             for i in range(len(st.session_state['generated'])):
#                 message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
#                 message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


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

# if __name__ == "__main__":
#     main()