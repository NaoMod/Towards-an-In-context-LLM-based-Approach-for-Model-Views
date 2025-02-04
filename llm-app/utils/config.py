import os

from langchain_openai import AzureChatOpenAI
# alternative models
from langchain_mistralai import ChatMistralAI 
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class Config:
    """
    Configuration class for managing keys and settings.

    Parameters
    ----------
    project_name : str, optional
        The name of the project. Default is "SLE-Presentation".

    Attributes
    ----------
    open_ai_key : str or None
        The Open AI key used for language translation.
    langsmith_key : str or None
        The LangSmith key used for configuring the environment variables.
    llm : ChatOpenAI, ChatMistralAI or None
        The LLM instance used for language translation.
    project_name : str
        The name of the project.

    Methods
    -------
    load_keys()
        Load the keys from the token file and configure the environment variables for LangSmith.
    get_llm()
        Get the LLM instance to be used during the execution.
    test_llm()
        Test the LLM functionality by sending messages to the LLM instance.
    """

    def __init__(self, project_name: str = "SLE-Presentation"):
        self.llm_name = os.getenv("LLM_NAME", "AzureChatOpenAI")
        self.open_ai_key = os.getenv("LLM_SECRET", None)
        self.langsmith_key = os.getenv("LANGSMITH_KEY", None)
        self.llm = None
        self.project_name = project_name
        self.temperature = os.getenv("LLM_TEMPERATURE", 0)

    def load_keys(self):
        """
        Configure the environment variables for LangSmith and configure the LLM.

        Returns
        -------
        None

        """        
        if self.langsmith_key is not None:
            # Configure LangSmith
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = self.project_name
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = self.langsmith_key

        if self.llm_name == "AzureChatOpenAI":
            self.llm = AzureChatOpenAI(
                azure_endpoint="https://models.inference.ai.azure.com",
                temperature=self.temperature,
                api_key=self.open_ai_key,
                openai_api_version="2024-09-01-preview", 
                model_name="gpt-4o")
        elif self.llm_name == "ChatMistralAI":
            self.llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=self.temperature,
                mistral_api_key=self.open_ai_key)
        elif self.llm_name == "ChatOllama":
            self.llm = ChatOllama(
                temperature=self.temperature,
                base_url=os.getenv("LLM_API_URL", "http://localhost:8000"),
                model_name="llama3")

    def get_llm(self):
        """
        Get the LLM instance to be used during the execution.

        Returns
        -------
        LLM
            The LLM instance.
        """
        return self.llm

    def test_llm(self):
        """
        Test the LLM functionality.

        This method sends a list of messages to the LLM instance for testing purposes.
        The messages include a system message and a human message to be translated from English to French.

        Returns
        -------
        BaseMessage
            The output of the LLM.
        """
        messages = [
            SystemMessage(
                content="You are a helpful assistant that translates English to French."
            ),
            HumanMessage(
                content="Translate this sentence from English to French. I love software modeling."
            ),
        ]
        return self.llm.invoke(messages, config={"tags": ["TEST"]})
